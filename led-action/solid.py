import sys
import neopixel
import board
import signal
import time
import os
from config import NUMBER_OF_LEDS, MAX_BRIGHTNESS


def hex_to_rgb(hex):
    if not len(hex) == 6:
        raise ValueError("Not a valid Hex Color")
    else:
        return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))


if __name__ == '__main__':
    try:
        custom_brightness = min(max(float(os.environ.get(
            "ls_c_brightness", str(MAX_BRIGHTNESS))), 0.05), 1)
    except ValueError:
        custom_brightness = MAX_BRIGHTNESS
    pixels = neopixel.NeoPixel(
        board.D18, NUMBER_OF_LEDS, brightness=custom_brightness)

    def sigterm_handler(_signo, _stack_frame):
        pixels.deinit()
        sys.exit(0)

    signal.signal(signal.SIGTERM, sigterm_handler)
    signal.signal(signal.SIGINT, sigterm_handler)

    color_hex = sys.argv[1]
    if not len(color_hex) == 6:
        print('invalid color: ' + color_hex)
        sys.exit(-1)

    pixels.fill(hex_to_rgb(color_hex))

    while True:
        time.sleep(2)
