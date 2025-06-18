# Contributing to acrome-lib

Thank you for your interest in contributing to **acrome-lib**! We welcome improvements, bug fixes, and new device wrappers. To ensure a smooth process, please follow these guidelines.

---

## Table of Contents

1. [Reporting Issues](#reporting-issues)
2. [Feature Requests](#feature-requests)
3. [Development Setup](#development-setup)
4. [Coding Standards](#coding-standards)
5. [Writing Tests](#writing-tests)
6. [Pull Request Process](#pull-request-process)
7. [Review & Merge](#review--merge)
8. [Code of Conduct](#code-of-conduct)

---

## Reporting Issues

If you encounter a bug or unexpected behavior:

1. Check existing [issues](https://github.com/MehmetBener/acrome-lib/issues) for related reports.
2. If none exist, open a new issue with:

   * A clear, descriptive title.
   * A detailed description of the problem.
   * Steps to reproduce the issue.
   * Environment information (OS, Python version, acrome-smd-python version).
   * Relevant logs or error messages.

Example:

````
Title: "Button wrapper .is_pressed() always returns False"

Description:
On Raspberry Pi 4 with acrome-smd-python v0.1.0, calling `Button.is_pressed()` never returns True even when the button is pressed.

Steps to reproduce:
1. Connect a Button_5 module to the USB gateway.
2. Run:
   ```python
   btn = Button(gw, module_id=0)
   while True:
       print(btn.is_pressed())
````

3. Press the button and observe the output.

````

---

## Feature Requests

For new features or enhancements:

1. Check for existing feature requests.
2. Open a new issue with:
   - A clear summary of the desired feature.
   - Motivation and use cases.
   - (Optional) Proposed API or code sketch.

---

## Development Setup

1. Fork the repository.
2. Clone your fork:
   ```bash
git clone https://github.com/<your-username>/acrome-lib.git
cd acrome-lib
````

3. Create and activate a virtual environment:

   ```bash
   ```

python3 -m venv venv
source venv/bin/activate

````
4. Install dependencies in editable mode:
```bash
pip install -e .[test]
````

5. Verify setup by running existing tests:

   ```bash
   ```

pytest --maxfail=1 --disable-warnings -v

````

---

## Coding Standards

- **Language**: Python 3.8+
- **Style**: Follow [PEP8](https://www.python.org/dev/peps/pep-0008/).
- Use 4 spaces per indent, max line length 79 characters.
- Write docstrings for all public classes and functions (Google style).
- **Imports**: Group imports in order: standard library, third-party, local modules.
- **Type hints**: Use type annotations for public APIs.
- **Formatting**: Run `black .` and `flake8 .` before committing.

---

## Writing Tests

- Place tests under `tests/` with filenames `test_<module>.py`.
- Use `pytest` for tests.
- Aim for comprehensive coverage of new features and edge cases.
- Include hardware-agnostic mocks if necessary (e.g., monkeypatch `MorseHardware`).

Example test skeleton:
```python
import pytest
from acrome_lib.led import RGBLed

def test_rgb_led_set_color(monkeypatch):
 class DummyGW:
     def __init__(self):
         self.cmds = []
     def set_rgb(self, smd_id, led_id, r, g, b):
         self.cmds.append((r, g, b))

 gw = DummyGW()
 led = RGBLed(gw, module_id=5)
 led.set_color(1, 2, 3)
 assert gw.cmds == [(1, 2, 3)]
````



