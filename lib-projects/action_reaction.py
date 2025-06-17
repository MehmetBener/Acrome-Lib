### lib-projects/action_reaction.py

import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import time
from lib.usb_port_finder import USBPortFinder
from lib.smd_gateway import SMDGateway, DEFAULT_MODULES
from lib.button import Button
from lib.led import Led

def main():
    port = USBPortFinder.first_gateway()
    if not port:
        print("No USB gateway.")
        sys.exit(1)
    gw  = SMDGateway(port, modules_override=DEFAULT_MODULES)
    btn = Button(gw, module_id=5)
    led = Led(gw, module_id=5)

    try:
        while True:
            if btn.is_pressed():
                led.on((255,0,0))  # Reaction: red on
            else:
                led.off()
            time.sleep(0.05)
    except KeyboardInterrupt:
        pass
    finally:
        gw.close()

if __name__ == "__main__":
    main()
