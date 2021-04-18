import time
import signal
import board
import neopixel
import sys
import math
from .config import NUMBER_OF_LEDS


def make_color_gradient(frequency1, frequency2, frequency3,
                        phase1, phase2, phase3,
                        center, width, len):
    # https://krazydad.com/tutorials/makecolors.php
    if (center is None):
        center = 128
    if (width is None):
        width = 127
    if (len is None):
        len = 60

    result = []

    for i in range(len):
        red = math.sin(frequency1*i + phase1) * width + center
        grn = math.sin(frequency2*i + phase2) * width + center
        blu = math.sin(frequency3*i + phase3) * width + center
        result.append((math.floor(red), math.floor(grn), math.floor(blu)))

    return result


if __name__ == '__main__':
    pixels = neopixel.NeoPixel(board.D18, NUMBER_OF_LEDS)

    def sigterm_handler(_signo, _stack_frame):
        pixels.deinit()
        sys.exit(0)

    signal.signal(signal.SIGTERM, sigterm_handler)
    signal.signal(signal.SIGINT, sigterm_handler)

    colors = make_color_gradient(.3, .3, .3, 0, 2, 4, None, None, None)

    for i in range(math.min(NUMBER_OF_LEDS, len(colors))):
        pixels[i] = colors[i]

    while True:
        time.sleep(2)
