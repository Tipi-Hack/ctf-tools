from PIL import Image

im1 = Image.open("one_too_many_1.png")
im2 = Image.open("one_too_many_2.png")
out = Image.new('RGB', (500, 180),"black")
pixels = out.load()

rgb_im1 = im1.convert('RGB')
rgb_im2 = im2.convert('RGB')
# size is 256 by 256
for x in xrange(0, 500):
    for y in xrange(0, 180):
        r1, g1, b1 = rgb_im1.getpixel((x, y))
        r2, g2, b2 = rgb_im2.getpixel((x, y))
        pixels[x, y] = (r1^r2, g1^g2, b1^b2)
out.show()