### lib/distance.py

class DistanceSensor:
    """
    Ultrasonic distance sensor module.

    Usage:
        dist = DistanceSensor(gateway, module_id)
        cm   = dist.read_cm()
    """
    def __init__(self, gateway, module_id: int):
        self._gw = gateway
        self._id = module_id

    def read_cm(self) -> float:
        return self._gw.get_distance(self._id)
