### lib/buzzer.py

import time
from typing import Iterable, Tuple, Optional

class Buzzer:
    """
    Buzzer module: tone, beep, and melody.
    """
    def __init__(self, gateway, module_id: int):
        self._gw = gateway
        self._id = module_id

    def _tone(self, freq: int):
        self._gw.set_buzzer(self._id, freq)

    def on(self, freq: int = 600):
        """Start continuous tone."""
        self._tone(freq)

    def off(self):
        """Stop tone."""
        self._tone(0)

    def beep(
        self,
        freq: int = 600,
        duration: float = 0.2,
        pause: float = 0.2,
        cycles: Optional[int] = 1
    ):
        """
        Beep `cycles` times at `freq` Hz.
        """
        try:
            for _ in range(cycles):
                self._tone(freq)
                time.sleep(duration)
                self._tone(0)
                time.sleep(pause)
        finally:
            self.off()

    def play(
        self,
        melody: Iterable[Tuple[int, float]],
        inter_note: float = 0.05
    ):
        """
        Play a sequence of (freq, duration) notes.
        """
        try:
            for freq, dur in melody:
                self._tone(freq)
                time.sleep(dur)
                self._tone(0)
                time.sleep(inter_note)
        finally:
            self.off()
