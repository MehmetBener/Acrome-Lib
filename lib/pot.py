### lib/pot.py
class Potentiometer:
    """
    Potentiometer (analog input).

    Usage:
        pot = Potentiometer(gateway, module_id)
        val = pot.read()
    """
    def __init__(self, gateway, module_id: int):
        self._gw = gateway
        self._id = module_id

    def read(self) -> int:
        return self._gw._master.get_pot(self._gw.device_id, self._id)
