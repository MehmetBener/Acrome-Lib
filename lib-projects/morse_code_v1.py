### lib-projects/morse_code.py

import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import time

from lib.usb_port_finder import USBPortFinder
from lib.smd_gateway import SMDGateway, DEFAULT_MODULES
from lib.led import Led
from lib.buzzer import Buzzer

# Morse code timing (seconds)
DOT_DURATION   = 0.1
DASH_DURATION  = DOT_DURATION * 3
SYMBOL_PAUSE   = DOT_DURATION
LETTER_PAUSE   = DOT_DURATION * 3
WORD_PAUSE     = DOT_DURATION * 7

# Basic A–Z, 0–9 mapping
MORSE_CODE = {
    'A': '.-',    'B': '-...',  'C': '-.-.', 'D': '-..',  'E': '.',
    'F': '..-.',  'G': '--.',   'H': '....', 'I': '..',   'J': '.---',
    'K': '-.-',   'L': '.-..',  'M': '--',   'N': '-.',   'O': '---',
    'P': '.--.',  'Q': '--.-',  'R': '.-.',  'S': '...',  'T': '-',
    'U': '..-',   'V': '...-',  'W': '.--',  'X': '-..-', 'Y': '-.--',
    'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---','3': '...--','4': '....-',
    '5': '.....', '6': '-....', '7': '--...','8': '---..','9': '----.'
}

def transmit_symbol(symbol: str, led: Led, buzzer: Buzzer):
    """Flash & beep a single dot or dash."""
    if symbol == '.':
        duration = DOT_DURATION 
    else: 
        duration = DASH_DURATION

    # ON
    led.on((255, 255, 255))
    buzzer.beep(freq=600, duration=duration)
    time.sleep(duration)

    # OFF
    led.off()
    time.sleep(SYMBOL_PAUSE)

def transmit_message(message: str, led: Led, buzzer: Buzzer):
    for word in message.strip().upper().split():
        for letter in word:
            code = MORSE_CODE.get(letter)
            if not code:
                continue  # skip unsupported chars
            for sym in code:
                transmit_symbol(sym, led, buzzer)
            # pause between letters
            time.sleep(LETTER_PAUSE - SYMBOL_PAUSE)
        # pause between words
        time.sleep(WORD_PAUSE - LETTER_PAUSE)

def main():
    port = USBPortFinder.first_gateway()
    if not port:
        print("No USB gateway detected.")
        sys.exit(1)

    # Only LED and Buzzer modules needed
    gw = SMDGateway(port, modules_override=DEFAULT_MODULES)
    led = Led(gw, module_id=5)
    buzzer = Buzzer(gw, module_id=5)

    try:
        msg = input("Enter message for Morse transmit: ")
        print(f"Transmitting: {msg}")
        transmit_message(msg, led, buzzer)
        print("Done.")
    except KeyboardInterrupt:
        print("\nInterrupted.")
    finally:
        gw.close()

if __name__ == "__main__":
    main()
