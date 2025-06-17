### lib/motor.py
import time
from smd.red import OperationMode

class Motor:
    def __init__(self, gateway, cpr: int):
        self._gw = gateway
        self.cpr = cpr

        # Optionally store default PID params or other state here
        # e.g. self._vel_pid = (p, i, d), etc.

        # Configure encoder CPR immediately
        self._gw.set_shaft_cpr(cpr)

    def configure_velocity_control(self, p: float, i: float, d: float):
        self._gw.set_control_parameters_velocity(p, i, d)

    def configure_position_control(self, p: float, i: float, d: float):
        self._gw.set_control_parameters_position(p, i, d)

    def configure_torque_control(self, p: float, i: float, d: float):
        self._gw.set_control_parameters_torque(p, i, d)

    def enable_torque(self, enabled: bool = True):
        self._gw.enable_torque(enabled)

    def set_operation_mode(self, mode: OperationMode):
        self._gw.set_operation_mode(mode)

    def set_shaft_rpm(self, rpm: float):
        self._gw.set_shaft_rpm(rpm)

    def set_pwm(self, duty: int):
        self._gw.set_duty_cycle(duty)

    # --- Higher-level actions ---

    def run_pwm(self, duty: int, duration_s: float = None):
        # Ensure mode is PWM
        self.set_operation_mode(OperationMode.PWM)
        self.enable_torque(True)
        self.set_pwm(duty)
        if duration_s is not None:
            time.sleep(duration_s)
            self.stop()

    def stop(self):
        # In PWM mode, zero duty
        try:
            # If in PWM mode:
            self.set_pwm(0)
        except Exception:
            pass
        # Also disable torque
        try:
            self.enable_torque(False)
        except Exception:
            pass

    def run_velocity(self, rpm: float):
        self.set_operation_mode(OperationMode.Velocity)
        self.enable_torque(True)
        try:
            self._gw._master.goVelocity(self._gw.device_id, rpm)
        except Exception:
            self.set_shaft_rpm(rpm)


    def run_position(self, position: float):
        self.set_operation_mode(OperationMode.Position)
        self.enable_torque(True)
        # Many SDKs: master.goTo(device_id, position) or set_position
        # Here we assume method is named goTo or set_position in gateway:
        # If SMDGateway had a wrapper:
        try:
            # Adjust as per actual SDK method name:
            self._gw._master.goTo(self._gw.device_id, position)
        except AttributeError:
            # If no goTo, comment or handle appropriately
            raise NotImplementedError("Position control method not implemented in gateway.")
