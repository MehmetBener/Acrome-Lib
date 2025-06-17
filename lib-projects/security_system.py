### lib-projects/security_system.py

import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import time
from lib.usb_port_finder import USBPortFinder
from lib.smd_gateway import SMDGateway
from lib.distance import DistanceSensor
from lib.led import Led
from lib.buzzer import Buzzer

ALERT_DIST = 30  # cm
BEEP_FREQ  = 1200  # Hz
BEEP_DUR   = 0.2   # seconds

def main():
    port = USBPortFinder.first_gateway()
    if not port:
        print("No USB gateway.")
        sys.exit(1)

    gw   = SMDGateway(port)
    dist = DistanceSensor(gw, module_id=1)
    led  = Led(gw, module_id=5)
    buzz = Buzzer(gw, module_id=5)

    try:
        while True:
            d = dist.read_cm()
            if d > 0 and d < ALERT_DIST:
                # turn the warning LED on
                led.on((255, 0, 0))
                # sound a single beep
                buzz.beep(freq=BEEP_FREQ, duration=BEEP_DUR)
            else:
                # clear outputs
                led.off()
            time.sleep(0.2)
    except KeyboardInterrupt:
        pass
    finally:
        gw.close()

if __name__ == "__main__":
    main()
