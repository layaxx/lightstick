import sys
import neopixel
import board
import signal
import time


class GracefulKiller:
    kill_now = False

    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, _, __):
        self.kill_now = True


if __name__ == '__main__':
    killer = GracefulKiller()
    pixels = neopixel.NeoPixel(board.D18, 60)
    while not killer.kill_now:
        for _ in range(10):
            for x in range(0, 50):
                pixels[x] = (200, 0, 0)
                time.sleep(0.1)
            for y in range(50):
                pixels[50-y] = (0, 0, 0)
                time.sleep(0.1)

    pixels.deinit()

    print("End of the program. I was killed gracefully :)")
