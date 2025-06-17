### lib/light.py

class LightSensor:
    """
    Ambient light sensor module.

    Usage:
        light = LightSensor(gateway, module_id)
        lux = light.read_lux()
    """
    def __init__(self, gateway, module_id: int):
        self._gw = gateway
        self._id = module_id

    def read_lux(self) -> float:
        return self._gw._master.get_light(self._gw.device_id, self._id)