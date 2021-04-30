import math


def make_color_gradient(frequency1, frequency2, frequency3,
                        phase1, phase2, phase3,
                        center, width, length):
    # https://krazydad.com/tutorials/makecolors.php
    if (center is None):
        center = 128
    if (width is None):
        width = 127
    if (length is None):
        length = 60

    result = []

    for i in range(length):
        red = math.sin(frequency1*i + phase1) * width + center
        grn = math.sin(frequency2*i + phase2) * width + center
        blu = math.sin(frequency3*i + phase3) * width + center
        result.append((math.floor(red), math.floor(grn), math.floor(blu)))

    return result
