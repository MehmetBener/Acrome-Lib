### lib/led.py
import time
from typing import Tuple, Optional

class Led:
    def __init__(self, gateway, module_id: int):
        self._gw = gateway
        self._id = module_id

    def _write(self, rgb: Tuple[int, int, int]):
        r, g, b = rgb
        self._gw.set_rgb(self._id, (r, g, b))

    def on(self, rgb: Tuple[int, int, int] = (255, 255, 255)):
        self._write(rgb)

    def off(self):
        self._write((0, 0, 0))

    def blink(self,
              on_rgb: Tuple[int, int, int] = (255, 0, 0),
              off_rgb: Tuple[int, int, int] = (0, 0, 0),
              period: float = 0.5,
              cycles: Optional[int] = None):
        print(f"[Led] Starting blink: on={on_rgb}, off={off_rgb}, period={period}, cycles={cycles}")
        try:
            n = 0
            while cycles is None or n < cycles:
                self._write(on_rgb)
                time.sleep(period)
                self._write(off_rgb)
                time.sleep(period)
                n += 1
        except KeyboardInterrupt:
            pass
        finally:
            self.off()
            print("[Led] blink finished, LED off")
