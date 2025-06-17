### lib/imu.py
from typing import Tuple

class Imu:
    """
    9-DoF IMU (accelerometer + gyroscope). Provides raw readings.

    Usage:
        imu = Imu(gateway, module_id)
        ax,ay,az = imu.read_accel()
        gx,gy,gz = imu.read_gyro()
    """
    def __init__(self, gateway, module_id: int):
        self._gw = gateway
        self._id = module_id

    def read_accel(self) -> Tuple[float, float, float]:
        return self._gw._master.get_accel(self._gw.device_id, self._id)

    def read_gyro(self) -> Tuple[float, float, float]:
        return self._gw._master.get_gyro(self._gw.device_id, self._id)
