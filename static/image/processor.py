import cv2
import numpy as np
from PIL import Image

# read image into matrix.
m = cv2.imread("/uploads/input.png")


# get image properties.
h, w, bpp = np.shape(m)

# iterate over the entire image.
# BLUE = 0, GREEN = 1, RED = 2.

for py in range(0, h):
    for px in range(0, w):
        # m[py][px][2] = 2
        n = m[py][px][2]
        Y = [n, 0, 0]
        m, Y = np.array(m), np.array(Y)
        m = np.absolute(m - Y)


y = 1
x = 1
print(m)
print(m[x][y])

# display image
# cv2.imshow('matrix', m)
# cv2.waitKey(0)
cv2.imwrite('new.jpeg', m)
img = Image.open('new.jpeg')
img.show()

img = Image.open('new.jpeg').convert('L')
img.save('new_gray_scale.jpg')
img.show()
