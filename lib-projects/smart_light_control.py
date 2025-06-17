### lib-projects/smart_light_control.py

import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import time
from lib.usb_port_finder import USBPortFinder
from lib.smd_gateway import SMDGateway, DEFAULT_MODULES
from lib.pot import Potentiometer
from lib.led import Led

def main():
    port = USBPortFinder.first_gateway()
    if not port:
        print("No USB gateway.")
        sys.exit(1)
    gw  = SMDGateway(port, modules_override=DEFAULT_MODULES)
    pot = Potentiometer(gw, module_id=5)
    led = Led(gw, module_id=5)

    try:
        while True:
            v = pot.read()  # 0.0–1.0
            print(v)
            intensity = int(v)
            led.on((intensity, intensity, 0))  # warm yellow dimming
            time.sleep(0.05)
    except KeyboardInterrupt:
        pass
    finally:
        gw.close()

if __name__ == "__main__":
    main()
