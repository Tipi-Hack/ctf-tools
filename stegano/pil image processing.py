# Very simple base script for using PIL to process an image and detect hidden pixels

import sys
from PIL import Image

# Reminder: PIL layout in im.load()
#   +---------------> X
#   | (0,0)      (255,0)
#   |
#   |
#   |
#   |
# Y v (0,255)    (255,255)
#

# in this challenge we had repetitive vertical bands of pixels
# +----------------------+
# | .... . ... ... .. . .|
# | . .. .. . . . ..... .|
# +----------------------+
#
#
# +----------------------+
# | .... . ... ... .. . .|
# | . .. .. . . . ..... .|
# +----------------------+
#
# We first had to collect only one band

im = Image.open("image.png")
pix = im.load()
w = im.size[0]
h = im.size[1]

prev_y = -1
pixels_in_band = []
for j in range(0, h):
    for i in range(0, w):
        # these loops scan first the first line, then the second line, and so on...
        if pix[i, j] != (255, 255, 255):
            x = i / 10  # we observed that all pixels coordinates can be divided by 10
            y = j / 10

            # first iteration
            if prev_y == -1:
                prev_y = y

            if y - prev_y > 2:
                # if the vertical delta between two pixels is too high, we are in the 2nd band
                # so let's stop
                min_x = 5000
                min_y = 5000
                max_x = 0
                max_y = 0
                for pix in pixels_in_band:
                    min_x = min(pix[0], min_x)
                    min_y = min(pix[1], min_y)
                    max_x = max(pix[0], max_x)
                    max_y = max(pix[1], max_y)

                print "Band is within : (%d,%d) and (%d,%d)" % (min_x, min_y, max_x, max_y)
                sys.exit()

            prev_y = y
            pixels_in_band.append((x, y))
            # print "[%d,%d]" % (x, y)
