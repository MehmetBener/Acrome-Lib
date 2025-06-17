### tests/motor_test.py

import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import sys
import time

from lib.usb_port_finder import USBPortFinder
from lib.smd_gateway import SMDGateway
from lib.motor import Motor

def main():
    port = USBPortFinder.first_gateway()
    if port is None:
        print("Error: No USB gateway detected. Please connect the SMD Red board.")
        sys.exit(1)

    # Initialize gateway
    gateway = SMDGateway(port, baudrate=115_200, device_id=0)

    # Create Motor instance; supply correct CPR for your encoder
    # Replace 6533 with your motor’s encoder CPR:
    motor = Motor(gateway, cpr=6533)

    # Configure PID parameters as needed
    motor.configure_velocity_control(p=30.0, i=5.0, d=0.0)
    motor.configure_position_control(p=0.5, i=0.0, d=20.0)
    motor.configure_torque_control(p=3.0, i=0.1, d=0.0)
    
    pwm = -90
    wait_dur = 0.5
    
    for i in range(2):
        motor.run_pwm(pwm, duration_s=wait_dur)
        
        time.sleep(wait_dur)
        
        motor.run_pwm(0, duration_s=wait_dur)

        time.sleep(wait_dur)
        
    # Clean up
    gateway.close()

if __name__ == "__main__":
    main()
