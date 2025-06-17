### lib/button.py

class Button:
    """
    Wrapper for a digital push-button module.

    Usage:
        btn = Button(gateway, module_id)
        state = btn.is_pressed()
    """
    def __init__(self, gateway, module_id: int):
        self._gw = gateway
        self._id = module_id

    def is_pressed(self) -> bool:
        # returns True if pressed (digital read)
        return bool(self._gw._master.get_button(self._gw.device_id, self._id))