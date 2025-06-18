import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import time
import threading
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
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
        ms = int(dur * 1000)
        self.master.set_buzzer(self.smd_id, self.buzzer_id, ms)
        time.sleep(dur)
        self.master.set_buzzer(self.smd_id, self.buzzer_id, 0)

    def close(self):
        ser = getattr(self.master, 'serial', None)
        if ser and hasattr(ser, 'close'):
            ser.close()

# Transmission logic
def transmit_symbol(symbol, hw):
    dur = DOT_DURATION if symbol == '.' else DASH_DURATION
    hw.led_on()
    hw.beep(dur)
    hw.led_off()
    time.sleep(SYMBOL_PAUSE)


def transmit_message(msg, hw, on_progress=None):
    cleaned = msg.strip().upper()
    symbols = [s for ch in cleaned if ch != ' ' for s in MORSE_CODE.get(ch, '')]
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

# GUI Application
class MorseGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Morse Code Transmitter")
        self.configure(bg="#2c3e50")
        self.resizable(False, False)

        port = find_usb_port()
        if not port:
            messagebox.showerror("Error", "No USB gateway detected.")
            self.destroy()
            sys.exit(1)
        self.hw = MorseHardware(port)

        # Style progress bar with simple high-contrast green
        style = ttk.Style(self)
        style.configure("Custom.Horizontal.TProgressbar", background="#27ae60")

        # Header
        header = tk.Label(self, text="🔊 Morse Code Transmitter", font=("Helvetica", 20, "bold"),
                          fg="white", bg=self['bg'])
        header.pack(pady=(15, 10))

        content = tk.Frame(self, bg=self['bg'])
        content.pack(padx=20, pady=10)

        # Message input
        lbl_msg = tk.Label(content, text="Enter message:", font=("Arial", 12), fg="#ecf0f1", bg=self['bg'])
        lbl_msg.grid(row=0, column=0, sticky="w")
        self.msg_var = tk.StringVar()
        entry = tk.Entry(content, textvariable=self.msg_var, width=40,
                         font=("Arial", 12), bg="#ecf0f1", fg="#2c3e50", insertbackground="#2c3e50")
        entry.grid(row=1, column=0, columnspan=2, pady=(0,10))
        entry.focus()
        self.msg_var.trace_add("write", self._update_code)

        # Morse code display
        lbl_code = tk.Label(content, text="Morse code:", font=("Arial", 12), fg="#ecf0f1", bg=self['bg'])
        lbl_code.grid(row=2, column=0, sticky="w")
        self.code_lbl = tk.Label(content, text="", font=("Courier", 10), fg="#f1c40f",
                                 bg=self['bg'], justify="left", wraplength=360)
        self.code_lbl.grid(row=3, column=0, columnspan=2, pady=(0,10))

        # Controls
        self.btn_tx = tk.Button(content, text="Transmit", font=("Arial", 12, "bold"),
                                bg="#27ae60", fg="black", activebackground="#229954",
                                width=12, command=self._start)
        self.btn_tx.grid(row=4, column=0, pady=10, sticky="e")

        self.progress = ttk.Progressbar(content, style="Custom.Horizontal.TProgressbar",
                                        mode="determinate", length=250)
        self.progress.grid(row=4, column=1, padx=(10,0), pady=10, sticky="w")

        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _update_code(self, *_):
        words = []
        for w in self.msg_var.get().strip().upper().split():
            letters = [MORSE_CODE.get(ch, '') for ch in w]
            words.append(' '.join(filter(None, letters)))
        self.code_lbl.config(text=' / '.join(words))

    def _start(self):
        msg = self.msg_var.get().strip()
        if not msg:
            messagebox.showinfo("Input", "Please enter a message to transmit.")
            return
        self.btn_tx.config(state="disabled")
        self.progress['value'] = 0
        threading.Thread(target=self._worker, args=(msg,), daemon=True).start()

    def _worker(self, msg):
        try:
            transmit_message(msg, self.hw, self._prog)
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            self.btn_tx.config(state="normal")
            self.progress['value'] = 0

    def _prog(self, p):
        self.progress['value'] = p

    def _on_close(self):
        self.hw.close()
        self.destroy()

def run()
    MorseGUI().mainloop()
