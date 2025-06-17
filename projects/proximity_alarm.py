### projects/proximity_alarm.py

import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import time
from lib.usb_port_finder import USBPortFinder
from lib.smd_gateway import SMDGateway
from lib.distance import DistanceSensor
from lib.led import Led
from lib.buzzer import Buzzer

def main():
    port = USBPortFinder.first_gateway()
    if not port:
        print("No USB gateway.")
        sys.exit(1)
    gw = SMDGateway(port)
    dist = DistanceSensor(gw, module_id=1)
    led  = Led(gw, module_id=5)
    buz  = Buzzer(gw, module_id=5)

    try:
        while True:
            if dist.read_cm() < 10:
                led.blink(on_rgb=(255,0,0), off_rgb=(0,0,0), period=0.2, cycles=5)
                buz.beep(freq=1000, duration=0.1, pause=0.1, cycles=10)
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        gw.close()

if __name__ == "__main__":
    main()
