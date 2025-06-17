### tests/button_test.py

import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import sys
from lib.usb_port_finder import USBPortFinder
from lib.smd_gateway import SMDGateway, DEFAULT_MODULES
from lib.button import Button

def main():
    port = USBPortFinder.first_gateway()
    if not port:
        print("No USB gateway.")
        sys.exit(1)
        
    gw = SMDGateway(port, modules_override=DEFAULT_MODULES)

    btn = Button(gw, 5)

    print("Button.is_pressed() →", btn.is_pressed())

    gw.close()

if __name__ == "__main__":
    main()
