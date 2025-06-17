### tests/usb_port_finder_test.py

import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lib.usb_port_finder import USBPortFinder

def main():
    port = USBPortFinder.first_gateway()
    if port:
        print("Found USB gateway on", port)
    else:
        print("No gateway detected")

if __name__ == "__main__":
    main()
