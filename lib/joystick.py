### lib/joystick.py

from typing import Tuple

class Joystick:
    """
    Joystick module: X/Y axes and a push-button.

    Usage:
        joy = Joystick(gateway, module_id)
        x, y = joy.read_axes()
        pressed = joy.is_pressed()
    """
    def __init__(self, gateway, module_id: int):
        self._gw = gateway
        self._id = module_id

    def read_axes(self) -> Tuple[int, int]:
        # Returns raw X and Y values
        return self._gw._master.get_joy(self._gw.device_id, self._id)

    def is_pressed(self) -> bool:
        return bool(self._gw._master.get_joy_button(self._gw.device_id, self._id))
