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

    color = sys.argv[1]
    if not len(color) == 6:
        print('invalid color: ' + color)
        sys.exit(-1)

    pixels.fill(color)

    while True:
        time.sleep(2)
