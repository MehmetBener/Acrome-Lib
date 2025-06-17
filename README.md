[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE.txt)

# acrome-lib

**acrome-lib** is a Python library for interfacing with the Acrome SMD Red hardware platform. It provides a high‑level `SMDGateway` class to manage the USB gateway and a collection of module wrappers for all supported add‑on devices (buttons, sensors, actuators, motors, etc.).

---

## Features

* **Automatic module discovery** (with fallback to `DEFAULT_MODULES`)
* **Convenient wrappers** for:

  * Digital inputs: Button, Joystick button
  * Analog inputs: Potentiometer, QTR line sensor array, Light sensor, Distance sensor, IMU (accelerometer & gyroscope)
  * Actuators: RGB LED, Buzzer, Motor (PWM, velocity, position, torque)
* **Extensible**: easily add new module types by following the wrapper pattern
* **Built‑in testing**: standalone test scripts under `tests/` ensure compatibility

---

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/MehmetBener/acrome-lib.git
   cd acrome-lib
   ```

2. (Optional) Install in editable mode:

   ```bash
   pip install -e .
   ```

3. Ensure you have the Acrome Python SDK (`smd.red`) installed via pip and your USB gateway drivers.

---

## Usage

### 1. Initialize the Gateway

```python
from smd_gateway import SMDGateway
from lib.usb_port_finder import USBPortFinder

# Auto‑detect the USB gateway
port = USBPortFinder.first_gateway()
if port is None:
    raise RuntimeError("No USB gateway connected")

# Create gateway (overriding auto‑scan with DEFAULT_MODULES)
gw = SMDGateway(port, modules_override=None)
```

### 2. Create and Use Module Wrappers

```python
from lib.button import Button
from lib.led import Led
from lib.distance import DistanceSensor
# ... other wrappers ...

# Example: Button on module index 0 (Button_5)
btn = Button(gw, module_id=0)
if btn.is_pressed():
    print("Button pressed!")

# Example: Blink LED (module index 7 = RGB_5)
led = Led(gw, module_id=7)
led.blink(on_rgb=(0,255,0), off_rgb=(0,0,0), period=0.3, cycles=5)

# Example: Read distance (module index 4 = Distance_1)
dist = DistanceSensor(gw, module_id=4)
print("Distance (cm):", dist.read_cm())
```

### 3. Motor Control

```python
from lib.motor import Motor
from smd.red import OperationMode

motor = Motor(gw, cpr=6533)

# PWM control
motor.run_pwm(duty=50, duration_s=1.0)

# Velocity control
motor.set_operation_mode(OperationMode.Velocity)
motor.enable_torque(True)
motor.set_shaft_rpm(120)

# Cleanup
gw.close()
```

---

## Testing

All module wrappers include standalone test scripts under `tests/`. To run tests:

```bash
cd acrome-lib
# Example: test the QTR sensor wrapper
env/bin/python tests/test_qtr.py
```

Each script auto‑adds the project root to `PYTHONPATH` and uses `modules_override` to fix module IDs.

---

## Contributing

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/YourFeature`.
3. Commit your changes: `git commit -m "Add your feature"`.
4. Push to your fork: `git push origin feature/YourFeature`.
5. Open a Pull Request.

Please run existing tests and add new ones for any functionality you introduce.

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE.txt) for details.

---
