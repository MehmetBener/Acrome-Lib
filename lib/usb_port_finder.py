### lib/usb_port_finder.py
from platform import system
from serial.tools.list_ports import comports
from typing import Optional

class USBPortFinder:
    """
    Auto-detects the Acrome USB gateway port.
    """
    CANDIDATES = {
        "Windows": ["USB Serial Port"],
        "Linux":   ["/dev/ttyUSB"],
        "Darwin": [
            "/dev/tty.usbserial", "/dev/tty.usbmodem",
            "/dev/tty.SLAB_USBtoUART", "/dev/tty.wchusbserial",
            "/dev/cu.usbserial",
        ],
    }

    @staticmethod
    def first_gateway() -> Optional[str]:
        os_name = system()
        for p in comports():
            if any(tag in p.device or tag in p.description
                   for tag in USBPortFinder.CANDIDATES.get(os_name, [])):
                print(f"✔ USB gateway found on {p.device}")
                return p.device
        return None