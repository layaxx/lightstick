import sys
import neopixel
import board
import signal
import time
from config import NUMBER_OF_LEDS

if __name__ == '__main__':
    pixels = neopixel.NeoPixel(board.D18, NUMBER_OF_LEDS)

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
