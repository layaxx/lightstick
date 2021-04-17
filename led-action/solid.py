import board
import neopixel
import time
import sys
pixels = neopixel.NeoPixel(board.D18, 60)

if __name__ == '__main__':
    color = sys.argv[1]
    if not len(color) == 6:
        print('invalid color: ' + color)
        sys.exit(-1)
    try:
        #pixels.fill(color)
        pass
        while True:
            time.sleep(2)
    finally:
        #pixels.deinit()
        sys.exit(0)
