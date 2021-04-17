import board
import neopixel
import time
import sys
pixels = neopixel.NeoPixel(board.D18, 60)

try:
    for _ in range(10):
        for x in range(0, 50):
            pixels[x] = (200, 0, 0)
            time.sleep(0.1)
        for y in range(50):
            pixels[50-y] = (0, 0, 0)
            time.sleep(0.1)
finally:
    pixels.deinit()
    sys.exit(0)
