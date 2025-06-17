# projects/melody.py

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import time

from lib.usb_port_finder import USBPortFinder
from lib.smd_gateway     import SMDGateway
from lib.buzzer          import Buzzer

# note → frequency (Hz)
NOTES = {
    'C4': 261, 'D4': 294, 'E4': 329, 'F4': 349,
    'G4': 392, 'A4': 440, 'B4': 493, 'C5': 523
}

# full "Twinkle Twinkle Little Star" melody
# (note, duration in seconds)
MELODY = [
    # Twinkle, twinkle, little star
    ('C4', 0.3), ('C4', 0.3), ('G4', 0.3), ('G4', 0.3),
    ('A4', 0.3), ('A4', 0.3), ('G4', 0.6),
    # How I wonder what you are
    ('F4', 0.3), ('F4', 0.3), ('E4', 0.3), ('E4', 0.3),
    ('D4', 0.3), ('D4', 0.3), ('C4', 0.6),
    # Up above the world so high
    ('G4', 0.3), ('G4', 0.3), ('F4', 0.3), ('F4', 0.3),
    ('E4', 0.3), ('E4', 0.3), ('D4', 0.6),
    # Like a diamond in the sky
    ('G4', 0.3), ('G4', 0.3), ('F4', 0.3), ('F4', 0.3),
    ('E4', 0.3), ('E4', 0.3), ('D4', 0.6),
    # Twinkle, twinkle, little star
    ('C4', 0.3), ('C4', 0.3), ('G4', 0.3), ('G4', 0.3),
    ('A4', 0.3), ('A4', 0.3), ('G4', 0.6),
    # How I wonder what you are
    ('F4', 0.3), ('F4', 0.3), ('E4', 0.3), ('E4', 0.3),
    ('D4', 0.3), ('D4', 0.3), ('C4', 0.6),
]

PAUSE_BETWEEN_NOTES = 0.1  # short gap between tones

def play_melody(buzzer: Buzzer):
    for note, dur in MELODY:
        freq = NOTES[note]
        buzzer.beep(freq=freq, duration=dur)
        time.sleep(PAUSE_BETWEEN_NOTES)

def main():
    port = USBPortFinder.first_gateway()
    if not port:
        print("❌ No USB gateway detected.")
        sys.exit(1)

    gw     = SMDGateway(port)
    buzzer = Buzzer(gw, module_id=5)

    print("Playing Twinkle Twinkle Little Star...")
    try:
        play_melody(buzzer)
        print("Done.")
    except KeyboardInterrupt:
        print("\nInterrupted.")
    finally:
        gw.close()

if __name__ == "__main__":
    main()