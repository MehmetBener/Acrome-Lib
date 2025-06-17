### tests/led_test.py

import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lib.usb_port_finder import USBPortFinder
from lib.smd_gateway import SMDGateway
from lib.led import Led
import time

def main():
    port = USBPortFinder.first_gateway()
    if not port:
        print("No USB gateway.")
        return

    # Optionally you can pass modules_override=DEFAULT_MODULES,
    # but since we baked that in, you don't need to.
    gw  = SMDGateway(port)
    led = Led(gw, module_id=5)

    # Now this WILL light:
    led.blink(on_rgb=(0,255,0), off_rgb=(255,0,0), period=0.5, cycles=3)

    gw.close()

if __name__ == "__main__":
    main()
