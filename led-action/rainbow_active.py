import time
import signal
import board
import neopixel
import sys
import os
from config import NUMBER_OF_LEDS, MAX_BRIGHTNESS
from rainbow_utility import make_color_gradient


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

    colors = make_color_gradient(
        0.11, 0.11, 0.11, 2, 4, 6, None, None, NUMBER_OF_LEDS)

    try:
        duration = int(sys.argv[1])
    except ValueError:
        duration = 60

    timeout = duration/NUMBER_OF_LEDS

    for color in colors:
        pixels.fill(color)
        time.sleep(timeout)

    while True:
        time.sleep(2)
