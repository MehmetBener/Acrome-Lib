### lib-projects/autonomous_lighting.py

import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import time
from lib.usb_port_finder import USBPortFinder
from lib.smd_gateway import SMDGateway, DEFAULT_MODULES
from lib.light import LightSensor
from lib.led import Led

THRESHOLD_LUX = 100  # below this, turn on light

def main():
    port = USBPortFinder.first_gateway()
    if not port:
        print("No USB gateway.")
        sys.exit(1)
    gw     = SMDGateway(port, modules_override=DEFAULT_MODULES)
    sensor = LightSensor(gw, module_id=1)
    led    = Led(gw, module_id=5)

    try:
        while True:
            lux = sensor.read_lux()
            if lux < THRESHOLD_LUX:
                led.on((255,255,255))  # bright white
            else:
                led.off()
            time.sleep(0.5)
    except KeyboardInterrupt:
        pass
    finally:
        gw.close()

if __name__ == "__main__":
    main()
