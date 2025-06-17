# projects/morse_code.py
#
# Tkinter GUI for Morse-code transmitter + live code display
# ----------------------------------------------------------
import os, sys, threading, time, tkinter as tk
from tkinter import ttk, messagebox

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lib.usb_port_finder import USBPortFinder
from lib.smd_gateway     import SMDGateway, DEFAULT_MODULES
from lib.led             import Led
from lib.buzzer          import Buzzer

# ─── Morse-code timing ─────────────────────────────────────────────────────────
DOT_DURATION   = 0.1
DASH_DURATION  = DOT_DURATION * 3
SYMBOL_PAUSE   = DOT_DURATION
LETTER_PAUSE   = DOT_DURATION * 3
WORD_PAUSE     = DOT_DURATION * 7

MORSE_CODE = {
    'A': '.-',    'B': '-...',  'C': '-.-.', 'D': '-..',  'E': '.',
    'F': '..-.',  'G': '--.',   'H': '....', 'I': '..',   'J': '.---',
    'K': '-.-',   'L': '.-..',  'M': '--',   'N': '-.',   'O': '---',
    'P': '.--.',  'Q': '--.-',  'R': '.-.',  'S': '...',  'T': '-',
    'U': '..-',   'V': '...-',  'W': '.--',  'X': '-..-', 'Y': '-.--',
    'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---','3': '...--','4': '....-',
    '5': '.....', '6': '-....', '7': '--...','8': '---..','9': '----.'
}

# ─── Hardware helpers ──────────────────────────────────────────────────────────
def transmit_symbol(symbol: str, led: Led, buzzer: Buzzer):
    dur = DOT_DURATION if symbol == '.' else DASH_DURATION
    led.on((255, 255, 255))
    buzzer.beep(freq=600, duration=dur)
    time.sleep(dur)
    led.off()
    time.sleep(SYMBOL_PAUSE)

def transmit_message(msg: str, led: Led, buzzer: Buzzer, on_progress=None):
    cleaned = msg.strip().upper()
    total   = sum(len(MORSE_CODE.get(c, '')) for c in cleaned if c != ' ')
    sent    = 0
    for word in cleaned.split():
        for ch in word:
            code = MORSE_CODE.get(ch, '')
            for sym in code:
                transmit_symbol(sym, led, buzzer)
                sent += 1
                if on_progress and total:
                    on_progress(int(sent / total * 100))
            time.sleep(LETTER_PAUSE - SYMBOL_PAUSE)
        time.sleep(WORD_PAUSE - LETTER_PAUSE)
    if on_progress:
        on_progress(100)

def to_morse_string(msg: str) -> str:
    """Return a dot/dash string for display, using spaces between letters and / between words."""
    words = []
    for word in msg.strip().upper().split():
        letters = [MORSE_CODE.get(ch, '') for ch in word]
        words.append(' '.join(filter(None, letters)))
    return ' / '.join(words)

# ─── Tkinter GUI ───────────────────────────────────────────────────────────────
class MorseGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Morse Code Transmitter")
        self.resizable(False, False)

        port = USBPortFinder.first_gateway()
        if not port:
            messagebox.showerror("Gateway Error", "No USB gateway detected.")
            self.destroy()
            sys.exit(1)

        self.gw     = SMDGateway(port, modules_override=DEFAULT_MODULES)
        self.led    = Led(self.gw, module_id=5)
        self.buzzer = Buzzer(self.gw, module_id=5)

        # ── Widgets ────────────────────────────────────────────────────────────
        ttk.Label(self, text="Enter message:").grid(row=0, column=0, padx=8, pady=(10,2), sticky="w")

        self.msg_var = tk.StringVar()
        entry        = ttk.Entry(self, textvariable=self.msg_var, width=42)
        entry.grid(row=1, column=0, columnspan=2, padx=8, sticky="ew")
        entry.focus()
        self.msg_var.trace_add("write", self._update_code_display)

        ttk.Label(self, text="Morse code:").grid(row=2, column=0, padx=8, pady=(6,2), sticky="w")
        self.code_lbl = tk.Label(self, text="", font=("Courier", 10), justify="left", wraplength=300, anchor="w")
        self.code_lbl.grid(row=3, column=0, columnspan=2, padx=8, sticky="w")

        self.tx_btn   = ttk.Button(self, text="Transmit", command=self._start_tx)
        self.tx_btn.grid(row=4, column=0, padx=8, pady=10, sticky="e")

        self.progress = ttk.Progressbar(self, mode="determinate", length=200)
        self.progress.grid(row=4, column=1, padx=(0,8), pady=10, sticky="w")

        self.protocol("WM_DELETE_WINDOW", self._on_close)

    # ── UI callbacks ──────────────────────────────────────────────────────────
    def _update_code_display(self, *_):
        self.code_lbl.config(text=to_morse_string(self.msg_var.get()))

    def _start_tx(self):
        msg = self.msg_var.get().strip()
        if not msg:
            messagebox.showinfo("Input Needed", "Please enter a message to send.")
            return
        self.tx_btn.state(["disabled"])
        self.progress["value"] = 0
        threading.Thread(target=self._tx_worker, args=(msg,), daemon=True).start()

    def _tx_worker(self, msg):
        try:
            transmit_message(msg, self.led, self.buzzer, self._update_progress)
        except Exception as e:
            messagebox.showerror("Transmission Error", str(e))
        finally:
            self.tx_btn.state(["!disabled"])
            self.progress["value"] = 0

    def _update_progress(self, pct):
        self.progress["value"] = pct

    def _on_close(self):
        try:
            self.gw.close()
        finally:
            self.destroy()

# ─── Main ────
if __name__ == "__main__":
    MorseGUI().mainloop()
