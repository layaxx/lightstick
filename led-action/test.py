import sys
import neopixel
import board
import signal
import time
import os
from config import NUMBER_OF_LEDS, MAX_BRIGHTNESS

if __name__ == '__main__':

    try:
        custom_brightness = min(max(float(os.environ.get(
            "ls_c_brightness", str(MAX_BRIGHTNESS))), 0.05), 1)
    except ValueError:
        custom_brightness = MAX_BRIGHTNESS

    pixels = neopixel.NeoPixel(board.D18, NUMBER_OF_LEDS, custom_brightness)

    def sigterm_handler(_signo, _stack_frame):
        pixels.deinit()
        sys.exit(0)

    signal.signal(signal.SIGTERM, sigterm_handler)
    signal.signal(signal.SIGINT, sigterm_handler)

    while True:
        for x in range(0, NUMBER_OF_LEDS):
            pixels[x] = (200, 0, 0)
            time.sleep(0.1)
        for y in range(NUMBER_OF_LEDS):
            pixels[NUMBER_OF_LEDS - 1 - y] = (0, 0, 0)
            time.sleep(0.1)
