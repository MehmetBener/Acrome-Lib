[![PyPI version](https://img.shields.io/pypi/v/acrome-smd-python.svg)](https://pypi.org/project/acrome-smd-python/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE.txt)

# acrome-lib

**acrome-lib** is a Python library for interfacing with the Acrome SMD Red hardware platform. It provides a high‑level gateway class to manage the USB gateway and a set of device wrappers for sensors, actuators, and inputs. The library is published on PyPI under the name **acrome-smd-python**.

---

## Table of Contents

1. [Features](#features)
2. [Installation](#installation)
3. [Quick Start](#quick-start)
4. [Core Concepts](#core-concepts)
5. [Module Wrappers](#module-wrappers)
6. [Example Applications](#example-applications)
7. [Contributing](#contributing)
8. [Changelog](#changelog)
9. [License](#license)

---

## Features

* **Auto-Discovery** of connected SMD modules (with fallback to a default list)
* **Unified API** for digital inputs, analog sensors, and actuators
* **Extensible architecture**: add new device wrappers easily
* **Thread-safe** serial communication over USB
* **GUI examples** for common demos (Simon Says, Morse Code)
* **PyPI package**: install via `pip install acrome-smd-python`

---

## Installation

Install the library from PyPI (package name: **acrome-smd-python**):

```bash
pip install acrome-smd-python
```

Or install from source:

```bash
git clone https://github.com/MehmetBener/acrome-lib.git
cd acrome-lib
pip install -e .
```

> **Requirements:**
>
> * Python 3.8 or newer
> * `pyserial` (installed automatically)
> * Acrome USB gateway drivers

---

## Quick Start

1. **Detect USB gateway**:

   ```python
   from acrome_lib.utils import find_usb_port
   from acrome_lib.gateway import SMDGateway

   port = find_usb_port()
   if port is None:
       raise RuntimeError("No USB gateway found")
   ```

2. **Initialize gateway**:

   ```python
   gw = SMDGateway(port)
   ```

3. **List modules**:

   ```python
   modules = gw.list_modules()
   print("Detected modules:", modules)
   ```

4. **Control devices**:

   ```python
   from acrome_lib.led import RGBLed
   from acrome_lib.buzzer import Buzzer

   # Blink LED (module index 5)
   led = RGBLed(gw, module_id=5)
   led.set_color(255, 0, 0)  # Red
   led.off()

   # Beep buzzer
   buzzer = Buzzer(gw, module_id=5)
   buzzer.beep(0.2)
   ```

---

## Core Concepts

### `SMDGateway`

Manages the USB serial connection and module scanning:

* `SMDGateway(port, modules_override=None)` — create gateway
* `gw.list_modules()` — return list of detected module identifiers
* `gw.close()` — close the serial port cleanly

### Base Device Wrapper

All device classes inherit from a common base:

* Constructor signature: `(gateway, module_id)`
* Common methods: `.read()`, `.write()`, `.is_attached`

---

## Module Wrappers

| Category     | Class            | Description                        |
| ------------ | ---------------- | ---------------------------------- |
| **Digital**  | `Button`         | Push button input                  |
|              | `JoystickBtn`    | Joystick press button              |
| **Analog**   | `Potentiometer`  | Rotary potentiometer               |
|              | `LightSensor`    | Ambient light measurement          |
|              | `DistanceSensor` | Ultrasonic distance measurement    |
|              | `QTRSensor`      | Infrared line sensor array         |
|              | `IMUSensor`      | Accelerometer & gyroscope          |
| **Actuator** | `RGBLed`         | 3-channel PWM LED                  |
|              | `Buzzer`         | Piezo buzzer module                |
|              | `Motor`          | DC motor (PWM, velocity, position) |


---

## Example Applications

* **Simon Says Game**: Memory-sequence GUI demo using LEDs and buzzer.
  Path: `examples/simon_says.py`
* **Morse Code Transmitter**: GUI for sending text as Morse via LED/buzzer.
  Path: `examples/morse_gui.py`

Use these as starting points for custom interfaces.

---

## Contributing

Contributions are welcome:

1. Fork the repo
2. Create a branch: `git checkout -b feature/YourFeature`
3. Commit: `git commit -m "Add YourFeature"`
4. Push: `git push origin feature/YourFeature`
5. Open a Pull Request

Refer to [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## Changelog

### v0.1.0 (2025-06-18)

* Initial PyPI release as **acrome-smd-python**
* Core `SMDGateway` and all module wrappers
* GUI examples: Simon Says & Morse Code
* CI workflow for testing, build & publish

---

## License

Distributed under the MIT License. See [LICENSE.txt](LICENSE.txt) for details.

---
