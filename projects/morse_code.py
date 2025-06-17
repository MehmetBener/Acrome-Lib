### projects/morse_code.py

import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import time
import threading
import tkinter as tk
from tkinter import ttk, messagebox
from serial.tools.list_ports import comports
from platform import system
from smd.red import Master, Red

# Morse-code timing
DOT_DURATION   = 0.2
DASH_DURATION  = DOT_DURATION * 3
SYMBOL_PAUSE   = DOT_DURATION
LETTER_PAUSE   = DOT_DURATION * 3
WORD_PAUSE     = DOT_DURATION * 7

# Morse lookup
def build_morse_map():
    return {
        'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
        'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
        'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
        'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
        'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
        'Z': '--..',
        '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
        '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.'
    }
MORSE_CODE = build_morse_map()

# Hardware layer
def find_usb_port():
    ports = list(comports())
    os_name = system()
    usb_names = {
        "Windows": ["USB Serial Port"],
        "Linux": ["/dev/ttyUSB"],
        "Darwin": ["/dev/tty.usbserial", "/dev/tty.usbmodem", "/dev/cu.usbserial"]
    }
    for port, desc, hwid in sorted(ports):
        if any(name in port or name in desc for name in usb_names.get(os_name, [])):
            return port
    return None

class MorseHardware:
    def __init__(self, port, baud=115200, smd_id=0, led_id=5, buzzer_id=5):
        self.master = Master(port, baud)
        self.master.attach(Red(smd_id))
        self.master.scan_modules(smd_id)
        self.smd_id = smd_id
        self.led_id = led_id
        self.buzzer_id = buzzer_id

    def led_on(self):
        self.master.set_rgb(self.smd_id, self.led_id, 255, 255, 255)

    def led_off(self):
        self.master.set_rgb(self.smd_id, self.led_id, 0, 0, 0)

    def beep(self, dur):
        # dur in seconds
        ms = int(dur * 1000)
        # Start beep
        self.master.set_buzzer(self.smd_id, self.buzzer_id, ms)
        time.sleep(dur)
        # Stop beep
        self.master.set_buzzer(self.smd_id, self.buzzer_id, 0)

    def close(self):
        ser = getattr(self.master, 'serial', None)
        if ser and hasattr(ser, 'close'):
            ser.close()

# Morse logic
def transmit_symbol(symbol, hw):
    dur = DOT_DURATION if symbol == '.' else DASH_DURATION
    hw.led_on()
    hw.beep(dur)
    hw.led_off()
    time.sleep(SYMBOL_PAUSE)

def transmit_message(msg, hw, on_progress=None):
    cleaned = msg.strip().upper()
    symbols = [sym for ch in cleaned if ch != ' ' for sym in MORSE_CODE.get(ch, '')]
    total = len(symbols)
    count = 0
    for word in cleaned.split():
        for ch in word:
            for sym in MORSE_CODE.get(ch, ''):
                transmit_symbol(sym, hw)
                count += 1
                if on_progress and total:
                    on_progress(int(count / total * 100))
            time.sleep(LETTER_PAUSE - SYMBOL_PAUSE)
        time.sleep(WORD_PAUSE - LETTER_PAUSE)
    if on_progress:
        on_progress(100)

# GUI
def to_morse_string(msg):
    words = []
    for word in msg.strip().upper().split():
        letters = [MORSE_CODE.get(ch, '') for ch in word]
        words.append(' '.join(filter(None, letters)))
    return ' / '.join(words)

class MorseGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Morse Code Transmitter")
        self.resizable(False, False)

        port = find_usb_port()
        if not port:
            messagebox.showerror("Error", "No USB gateway detected.")
            self.destroy()
            sys.exit(1)
        self.hw = MorseHardware(port)

        ttk.Label(self, text="Enter message:").grid(row=0, column=0, padx=8, pady=(10, 2), sticky="w")
        self.msg_var = tk.StringVar()
        entry = ttk.Entry(self, textvariable=self.msg_var, width=42)
        entry.grid(row=1, column=0, columnspan=2, padx=8, sticky="ew")
        entry.focus()
        self.msg_var.trace_add("write", self._update_code)

        ttk.Label(self, text="Morse code:").grid(row=2, column=0, padx=8, pady=(6, 2), sticky="w")
        self.code_lbl = tk.Label(self, text="", font=("Courier", 10), justify="left", wraplength=300)
        self.code_lbl.grid(row=3, column=0, columnspan=2, padx=8, sticky="w")

        self.tx_btn = ttk.Button(self, text="Transmit", command=self._start)
        self.tx_btn.grid(row=4, column=0, padx=8, pady=10, sticky="e")
        self.progress = ttk.Progressbar(self, mode="determinate", length=200)
        self.progress.grid(row=4, column=1, padx=(0, 8), pady=10, sticky="w")
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _update_code(self, *_):
        self.code_lbl.config(text=to_morse_string(self.msg_var.get()))

    def _start(self):
        msg = self.msg_var.get().strip()
        if not msg:
            messagebox.showinfo("Input", "Enter a message.")
            return
        self.tx_btn.state(["disabled"])
        self.progress["value"] = 0
        threading.Thread(target=self._worker, args=(msg,), daemon=True).start()

    def _worker(self, msg):
        try:
            transmit_message(msg, self.hw, self._prog)
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            self.tx_btn.state(["!disabled"])
            self.progress["value"] = 0

    def _prog(self, p):
        self.progress["value"] = p

    def _on_close(self):
        self.hw.close()
        self.destroy()

if __name__ == '__main__':
    MorseGUI().mainloop()
