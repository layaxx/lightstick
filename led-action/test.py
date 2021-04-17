import sys
import neopixel
import board
import signal
import time


if __name__ == '__main__':
    pixels = neopixel.NeoPixel(board.D18, 60)

    def sigterm_handler(_signo, _stack_frame):
        pixels.deinit()
        sys.exit(0)

    signal.signal(signal.SIGTERM, sigterm_handler)
    signal.signal(signal.SIGINT, sigterm_handler)

    while True:
        for _ in range(10):
            for x in range(0, 50):
                pixels[x] = (200, 0, 0)
                time.sleep(0.1)
            for y in range(50):
                pixels[50-y] = (0, 0, 0)
                time.sleep(0.1)
