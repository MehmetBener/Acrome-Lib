### lib/smd_gateway.py

import time
from typing import Optional, Tuple, List
from smd.red import Master, Red, Index, OperationMode

# If scan_modules() ever returns [] or None, we'll fall back
# to this hard-coded list of your nine add-on modules:
DEFAULT_MODULES = [
    'Button_5', 'Light_5', 'Buzzer_5',
    'Joystick_5', 'Distance_1', 'QTR_1',
    'Pot_5',    'RGB_5',   'IMU_5'
]

class SMDGateway:
    def __init__(
        self,
        port: str,
        baudrate: int = 115200,
        device_id: int = 0,
        scan_timeout: float = 0.1,
        modules_override: Optional[List[str]] = None,
    ):
        """
        port, baudrate, device_id: as before.
        scan_timeout: how long to wait after enabling scan engine.
        modules_override: optional list of module names to register
                          (skips the auto-scan entirely).
        """
        self._master = Master(port, baudrate)
        self.device_id = device_id

        # Attach the Red protocol
        self._master.attach(Red(device_id))

                        # Monkey-patch missing Master methods for sensors:
        def _idx(key: str):
            for m in Index:
                if key.lower() in m.name.lower():
                    return m
            raise AttributeError(f"No Index member matching '{key}'")

                # Monkey-patch missing Master methods for sensors:
        def _idx(key: str):
            for m in Index:
                if key.lower() in m.name.lower():
                    return m
            raise AttributeError(f"No Index member matching '{key}'")

        # QTR (raw reflectance)
        try:
            qtr_idx = _idx('qtr')
            def read_qtr(dev_id, module_id):
                # module_id is already tracked by connection
                return list(self._master.get_variables(dev_id, [qtr_idx])[0])
            self._master.read_qtr = read_qtr
        except AttributeError:
            print("⚠ Index for QTR not found; QTR sensor methods unavailable.")

        # QTR position
        try:
            qtr_pos_idx = _idx('position')
            def read_qtr_position(dev_id, module_id):
                return self._master.get_variables(dev_id, [qtr_pos_idx])[0]
            self._master.read_qtr_position = read_qtr_position
        except AttributeError:
            print("⚠ Index for QTRPosition not found; QTR position method unavailable.")

        # Potentiometer
        try:
            pot_idx = _idx('pot')
            def get_pot(dev_id, module_id):
                return self._master.get_variables(dev_id, [pot_idx])[0]
            self._master.get_pot = get_pot
        except AttributeError:
            print("⚠ Index for Pot not found; potentiometer method unavailable.")

        # Joystick axes
        try:
            joy_idx = _idx('joy')
            def get_joy(dev_id, module_id):
                vals = self._master.get_variables(dev_id, [joy_idx])[0]
                # some SDKs pack axes
                if isinstance(vals, (list, tuple)):
                    return tuple(vals)
                return (vals >> 8, vals & 0xFF)
            self._master.get_joy = get_joy
        except AttributeError:
            print("⚠ Index for Joy not found; joystick axes unavailable.")

        # Joystick button
        try:
            joybtn_idx = _idx('button')
            def get_joy_button(dev_id, module_id):
                return self._master.get_variables(dev_id, [joybtn_idx])[0]
            self._master.get_joy_button = get_joy_button
        except AttributeError:
            print("⚠ Index for JoyButton not found; joystick button unavailable.")

        # IMU accelerometer
        try:
            accel_idx = _idx('accel')
            def get_accel(dev_id, module_id):
                vals = self._master.get_variables(dev_id, [accel_idx])[0]
                return tuple(vals) if isinstance(vals, (list, tuple)) else (vals,)
            self._master.get_accel = get_accel
        except AttributeError:
            print("⚠ Index for Accel not found; IMU accel unavailable.")

        # IMU gyroscope
        try:
            gyro_idx = _idx('gyro')
            def get_gyro(dev_id, module_id):
                vals = self._master.get_variables(dev_id, [gyro_idx])[0]
                return tuple(vals) if isinstance(vals, (list, tuple)) else (vals,)
            self._master.get_gyro = get_gyro
        except AttributeError:
            print("⚠ Index for Gyro not found; IMU gyro unavailable.")

        # Decide module list to register
        if modules_override is not None:
            modules = modules_override
            print(f"✔ Using override modules list: {modules}")
        else:
            self._master.set_variables(
                device_id,
                [[Index.SetScanModuleMode, 1]]
            )
            time.sleep(scan_timeout)

            modules = self._master.scan_modules(device_id) or []
            print(f"✔ scan_modules({device_id}) → {modules}")

            if not modules:
                modules = DEFAULT_MODULES.copy()
                print(f"⚠ scan failed, falling back to DEFAULT_MODULES: {modules}")

        self._master.set_connected_modules(device_id, modules)
        print(f"✅ Registered modules: {modules}")

    # Convenience wrappers
    def set_rgb(self, module_id: int, rgb: Tuple[int, int, int]):
        r, g, b = rgb
        self._master.set_rgb(self.device_id, module_id, r, g, b)

    def set_buzzer(self, module_id: int, freq_hz: int):
        self._master.set_buzzer(self.device_id, module_id, freq_hz)

    def get_distance(self, module_id: int):
        return self._master.get_distance(self.device_id, module_id)

    # Motor helpers
    def set_shaft_cpr(self, cpr: int):
        self._master.set_shaft_cpr(self.device_id, cpr)

    def set_shaft_rpm(self, rpm: float):
        self._master.set_shaft_rpm(self.device_id, rpm)

    def set_operation_mode(self, mode: OperationMode):
        self._master.set_operation_mode(self.device_id, mode)

    def set_control_parameters_velocity(self, p: float, i: float, d: float):
        self._master.set_control_parameters_velocity(self.device_id, p, i, d)

    def set_control_parameters_position(self, p: float, i: float, d: float):
        self._master.set_control_parameters_position(self.device_id, p, i, d)

    def set_control_parameters_torque(self, p: float, i: float, d: float):
        self._master.set_control_parameters_torque(self.device_id, p, i, d)

    def enable_torque(self, enabled: bool = True):
        self._master.enable_torque(self.device_id, enabled)

    def set_duty_cycle(self, duty: int):
        self._master.set_duty_cycle(self.device_id, duty)

    def close(self):
        try:
            self._master.close()
        except AttributeError:
            pass
