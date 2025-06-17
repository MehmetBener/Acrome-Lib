### tests/buzzer_test.py

import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lib.usb_port_finder import USBPortFinder
from lib.smd_gateway import SMDGateway
from lib.buzzer import Buzzer

def main():
    port = USBPortFinder.first_gateway()
    if not port:
        print("No USB gateway.")
        return

    gw  = SMDGateway(port)
    bz  = Buzzer(gw, module_id=5)

    # And now this WILL beep:
    bz.beep(freq=800, duration=0.3, pause=0.2, cycles=4)

    gw.close()

if __name__ == "__main__":
    main()
