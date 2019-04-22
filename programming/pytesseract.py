import cStringIO
import multiprocessing
import re
import time
from bs4 import BeautifulSoup

import requests
from PIL import Image, ImageOps
from pytesseract import pytesseract


def find_number(i, img, return_dict):
    image_data = re.sub('^data:image/.+;base64,', '', img).decode('base64')
    image = Image.open(cStringIO.StringIO(image_data))
    result = pytesseract.image_to_string(image, config="-c tessedit_char_whitelist=0123456789abcdef --psm 7")
    return_dict[i] = int(result, 16)


s = requests.Session()
r = s.get('http://FIXME/')

response = r.text
soup = BeautifulSoup(response, 'html.parser')
result = []
all_img = soup.find_all('img')

manager = multiprocessing.Manager()
return_dict = manager.dict()
jobs = []
for i, img in enumerate(all_img):
    p = multiprocessing.Process(target=find_number, args=(i, img.attrs['src'], return_dict))
    jobs.append(p)
    p.start()

for proc in jobs:
    proc.join()

total = 0
for d in return_dict.values():
    total += d
r = s.post('http://FIXME:9003/', data={"string": "%x" % total})
print(r.text)
