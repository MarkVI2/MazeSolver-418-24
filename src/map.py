from math import ceil
from PIL import Image
import cv2
import numpy as np


def noOfNodes(img, w, h):
    # counting the width of an "average" square
    width, white = 0, 0
    for x in range(w):
        for y in range(1):
            r, g, b = img.getpixel((x, y))
            if (r == 255 and g == 255 and b == 255):
                width += 1
                if (r != 255 and g != 255 and b != 255):
                    break

    # counting the number of white pixels in the entire maze
    for x in range(w):
        for y in range(h):
            r, g, b = img.getpixel((x, y))
            if (r == 255 and g == 255 and b == 255):
                white += 1

    if width == 0:
        return width, white, 0

    return width, white, ceil(white/pow(width, 2))


IMAGE_PATH = "input.png"

img = Image.open(IMAGE_PATH).convert('RGB')
w, h = img.size

width, white, nodes = noOfNodes(img, w, h)


if (10000 < nodes <= 50000):
    factor = 1/2
elif (nodes <= 100000):
    factor = 1/4
else:
    factor = 1/10

print(nodes)

if (nodes > 10000):
    w *= factor
    h *= factor
    img = np.array(img)
    dsize = (int(w), int(h))
    img_factored_down = cv2.resize(
        img, dsize, interpolation=cv2.INTER_LANCZOS4)
    img_factored_down = Image.fromarray(img_factored_down)
    width, white, nodes = noOfNodes(img_factored_down, int(w), int(h))
    img_factored_down.save("process_image.png")
    print(nodes)
    exit(0)

img.save("process_image.png")
