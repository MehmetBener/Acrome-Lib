import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import time
import random
import tkinter as tk
from tkinter import messagebox
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

    def beep(self, duration=0.2):
        ms = int(duration * 1000)
        self.master.set_buzzer(self.smd_id, self.buzzer_id, ms)
        time.sleep(duration)
        self.master.set_buzzer(self.smd_id, self.buzzer_id, 0)

    def close(self):
        ser = getattr(self.master, 'serial', None)
        if ser and hasattr(ser, 'close'):
            ser.close()

# ─── Simon Says GUI ────────────────────────────────────────────────────────────
# Restore original LED values
COLORS = [
    ("Red",   (255, 0,   0)),
    ("Green", (0,   255, 0)),
    ("Blue",  (0,   0,   255))
]

class SimonSaysApp(tk.Tk):
    def __init__(self, device):
        super().__init__()
        self.device = device
        self.title("🎮 Simon Says")
        self.configure(bg="#2c3e50")
        self.resizable(False, False)

        self.sequence = []
        self.user_index = 0

        # Initial power-up flash
        self.device.led_color(*COLORS[0][1])
        self.device.beep(0.7)
        self.device.led_off()
        time.sleep(1.0)

        self._build_ui()

    def _build_ui(self):
        # Header
        header = tk.Label(self, text="Simon Says", font=("Helvetica", 28, "bold"), fg="white", bg=self['bg'])
        header.pack(pady=(20, 10))

        # Status / Round
        self.status = tk.Label(self, text="Press Start to Play", font=("Helvetica", 16), fg="#ecf0f1", bg=self['bg'])
        self.status.pack(pady=(0,20))

        # Button Frame
        btn_frame = tk.Frame(self, bg=self['bg'])
        btn_frame.pack(pady=10)

        self.buttons = []
        for i, (name, color) in enumerate(COLORS):
            hexc = "#%02x%02x%02x" % color
            btn = tk.Button(
                btn_frame, text=name, bg=hexc, fg="black",  # use black text for contrast
                font=("Arial", 14, "bold"), width=10, height=4,
                bd=4, relief="raised",
                activebackground="white",
                command=lambda i=i: self._user_press(i)
            )
            btn.grid(row=0, column=i, padx=10)
            self.buttons.append((btn, color))

        # Control Frame
        control = tk.Frame(self, bg=self['bg'])
        control.pack(pady=20)

        self.start_btn = tk.Button(
            control, text="Start", font=("Helvetica", 14, "bold"),
            bg="#f39c12", fg="white", bd=3, relief="raised",
            activebackground="#e67e22", width=12, height=2,
            command=self._start_game
        )
        self.start_btn.pack()

    def _start_game(self):
        self.sequence.clear()
        self.start_btn.config(state="disabled")
        self._next_round()

    def _next_round(self):
        self.user_index = 0
        self.sequence.append(random.randrange(len(COLORS)))
        self.status.config(text=f"Round {len(self.sequence)} – Watch…")
        self.after(600, self._play_sequence, 0)

    def _play_sequence(self, idx):
        if idx < len(self.sequence):
            self._flash(self.sequence[idx])
            self.after(800, self._play_sequence, idx+1)
        else:
            self.status.config(text="Your Turn!")

    def _flash(self, idx):
        _, color = self.buttons[idx]
        self.device.led_color(*color)
        self.device.beep(0.3)
        self.buttons[idx][0].configure(relief="sunken")
        self.after(300, lambda b=self.buttons[idx][0]: b.configure(relief="raised"))
        self.after(200, self.device.led_off)

    def _user_press(self, idx):
        if not self.sequence:
            return
        self._flash(idx)
        if idx == self.sequence[self.user_index]:
            self.user_index += 1
            if self.user_index == len(self.sequence):
                self.status.config(text="✔ Correct! Next Round…")
                self.after(1000, self._reset_for_next)
        else:
            self.status.config(text="✖ Wrong! Game Over")
            messagebox.showinfo("Game Over", f"You reached round {len(self.sequence)}.")
            self.sequence.clear()
            self.start_btn.config(state="normal")

    def _reset_for_next(self):
        self.status.config(text="Great! Get Ready…")
        self.after(800, self._next_round)

# ─── Main ─────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    port = find_usb_port()
    if not port:
        print("No USB gateway detected.")
        sys.exit(1)

    device = Device(port)
    app = SimonSaysApp(device)
    app.protocol("WM_DELETE_WINDOW", lambda: (device.close(), app.destroy()))
    app.mainloop()
