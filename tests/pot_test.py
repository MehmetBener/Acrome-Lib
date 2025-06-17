### tests/pot_test.py

import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import sys
from lib.usb_port_finder import USBPortFinder
from lib.smd_gateway import SMDGateway, DEFAULT_MODULES
from lib.pot import Potentiometer

def main():
    port = USBPortFinder.first_gateway()
    if not port:
        print("No USB gateway.")
        sys.exit(1)
    gw = SMDGateway(port, modules_override=DEFAULT_MODULES)

    pot = Potentiometer(gw, module_id=5)
    print("Potentiometer value:", pot.read())

    gw.close()

if __name__ == "__main__":
    main()
