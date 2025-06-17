### projects/smart_doorbell.py

import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import sys, time
from lib.usb_port_finder import USBPortFinder
from lib.smd_gateway import SMDGateway
from lib.button import Button
from lib.buzzer import Buzzer
from lib.led import Led

def main():
    port = USBPortFinder.first_gateway()
    if not port:
        print("No USB gateway.")
        sys.exit(1)
    gw   = SMDGateway(port)
    btn  = Button(gw, module_id=5)
    buzz = Buzzer(gw, module_id=5)
    led  = Led(gw, module_id=5)

    try:
        while True:
            if btn.is_pressed():
                # chime
                for _ in range(3):
                    buzz.beep(freq=1000, duration=0.1, pause=0.1)
                # flash LED
                for _ in range(5):
                    led.on((0,0,255))
                    time.sleep(0.1)
                    led.off()
                    time.sleep(0.1)
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        gw.close()

if __name__ == "__main__":
    main()
