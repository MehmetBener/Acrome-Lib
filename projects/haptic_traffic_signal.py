# projects/haptic_traffic_signal.py

import os, sys
import time

# allow import from repo root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lib.usb_port_finder import USBPortFinder
from lib.smd_gateway     import SMDGateway
from lib.led             import Led
from lib.motor           import Motor

# Module IDs / parameters
LED_ID       = 5      # RGB LED module
CPR          = 6533   # motor encoder CPR
VIBRATION_DUTY  = 60  # PWM duty cycle for vibration
VIBRATION_DUR   = 0.2 # seconds motor vibrates on phase change

# Traffic light phase durations (seconds)
GREEN_DURATION  = 5
YELLOW_DURATION = 2
RED_DURATION    = 5

GREEN = (0,255,0)
YELLOW = (255,20,0)
RED = (255,0,0)

def vibrate(motor: Motor):
    """Briefly run the motor to simulate a haptic buzz."""
    motor.run_pwm(duty=VIBRATION_DUTY, duration_s=VIBRATION_DUR)

def main():
    port = USBPortFinder.first_gateway()
    if not port:
        print("❌ No USB gateway detected.")
        sys.exit(1)

    gw    = SMDGateway(port)
    led   = Led(gw, module_id=LED_ID)
    motor = Motor(gw, cpr=CPR)

    try:
        while True:
            # RED
            led.on(RED)
            time.sleep(RED_DURATION)
            vibrate(motor)

            # YELLOW
            led.on(YELLOW)
            time.sleep(YELLOW_DURATION)
            vibrate(motor)

            # GREEN
            led.on(GREEN)
            time.sleep(GREEN_DURATION)
            vibrate(motor)
    except KeyboardInterrupt:
        pass
    finally:
        # cleanup
        led.off()
        motor.run_pwm(duty=0, duration_s=0)
        gw.close()

if __name__ == "__main__":
    main()
