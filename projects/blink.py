### projects/blink.py

import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import sys, time
from lib.usb_port_finder import USBPortFinder
from lib.smd_gateway import SMDGateway
from lib.led import Led

def main():
    port = USBPortFinder.first_gateway()
    if not port:
        print("No USB gateway.")
        sys.exit(1)
    gw  = SMDGateway(port)
    led = Led(gw, module_id=5)

    try:
        while True:
            led.on((0,255,0))   # ON (green)
            time.sleep(0.5)
            led.off()           # OFF
            time.sleep(0.5)
    except KeyboardInterrupt:
        pass
    finally:
        gw.close()

if __name__ == "__main__":
    main()
