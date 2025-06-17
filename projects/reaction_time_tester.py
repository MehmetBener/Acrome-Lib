### projects/reaction_time_tester.py

import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import time
import random
import threading
import tkinter as tk
from tkinter import ttk, messagebox
from serial.tools.list_ports import comports
from platform import system
from smd.red import Master, Red

# ─── Hardware Layer ───────────────────────────────────────────────────────────
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

class Device:
    def __init__(self, port, baud=115200, smd_id=0, led_id=5, buzzer_id=5):
        self.master = Master(port, baud)
        self.master.attach(Red(smd_id))
        self.master.scan_modules(smd_id)
        self.smd_id = smd_id
        self.led_id = led_id
        self.buzzer_id = buzzer_id

    def led_color(self, r, g, b):
        self.master.set_rgb(self.smd_id, self.led_id, r, g, b)

    def led_off(self):
        self.led_color(0, 0, 0)

    def beep(self, duration=0.1):
        ms = int(duration * 1000)
        self.master.set_buzzer(self.smd_id, self.buzzer_id, ms)
        time.sleep(duration)
        self.master.set_buzzer(self.smd_id, self.buzzer_id, 0)

    def close(self):
        ser = getattr(self.master, 'serial', None)
        if ser and hasattr(ser, 'close'):
            ser.close()

# ─── Reaction-Time Tester GUI ─────────────────────────────────────────────────
class ReactionTesterApp(tk.Tk):
    def __init__(self, device):
        super().__init__()
        self.title("Reaction-Time Tester")
        self.resizable(False, False)
        self.device = device

        # state flags
        self.test_active = False
        self.start_time = None

        self._build_ui()

    def _build_ui(self):
        self.status = ttk.Label(self, text="Press Start to begin")
        self.status.pack(padx=10, pady=(10,5))

        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=5)

        self.start_btn = ttk.Button(btn_frame, text="Start", command=self._start_test)
        self.start_btn.grid(row=0, column=0, padx=5)

        self.stop_btn = ttk.Button(btn_frame, text="Stop", command=self._stop_test, state="disabled")
        self.stop_btn.grid(row=0, column=1, padx=5)

    def _start_test(self):
        # enable test
        self.test_active = True
        self.start_time = None

        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="enabled")
        self.status.config(text="Get Ready...")

        # schedule the GO signal
        delay = random.uniform(1, 3)
        threading.Thread(target=self._wait_and_signal, args=(delay,), daemon=True).start()

    def _wait_and_signal(self, delay):
        time.sleep(delay)
        if not self.test_active:
            # user stopped too early, abort signal
            return

        # GO: light, beep, record time
        self.device.led_color(0, 255, 0)
        self.start_time = time.time()
        self.device.beep(0.1)
        # update UI
        self.after(0, lambda: self.status.config(text="GO!"))

    def _stop_test(self):
        if not self.test_active:
            return

        if not self.start_time:
            # Stopped too early
            self.test_active = False
            messagebox.showwarning("Too Soon", "You stopped too early! Try again.")
            self._reset()
            return

        # Valid stop
        rt_ms = int((time.time() - self.start_time) * 1000)
        self.status.config(text=f"Reaction: {rt_ms} ms")

        # feedback beeps
        for _ in range(max(1, rt_ms // 100)):
            self.device.beep(0.05)
            time.sleep(0.05)

        self._reset()

    def _reset(self):
        self.test_active = False
        self.start_time = None
        self.device.led_off()
        self.start_btn.config(state="enabled")
        self.stop_btn.config(state="disabled")
        self.status.config(text="Press Start to begin")

# ─── Main ─────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    port = find_usb_port()
    if not port:
        print("No USB gateway detected.")
        sys.exit(1)

    device = Device(port)
    app = ReactionTesterApp(device)
    app.protocol("WM_DELETE_WINDOW", lambda: (device.close(), app.destroy()))
    app.mainloop()
