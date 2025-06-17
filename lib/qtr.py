### lib/qtr.py
class QTRArray:
    """
    QTR line sensor array (reflectance sensors).

    Usage:
        qtr = QTRArray(gateway, module_id)
        values = qtr.read_all()
        pos    = qtr.read_position()
    """
    def __init__(self, gateway, module_id: int):
        self._gw = gateway
        self._id = module_id

    def read_all(self) -> list:
        return list(self._gw._master.read_qtr(self._gw.device_id, self._id))

    def read_position(self) -> float:
        return self._gw._master.read_qtr_position(self._gw.device_id, self._id)
