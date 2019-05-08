from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from libdeda.privacy import AnonmaskApplierTdm
from libdeda.pattern_handler import TDM, Pattern4
from datetime import datetime
import pyotp
from base64 import b32encode

from fpdf import FPDF
import pdf2image

otp_seed = 83427324
otp = pyotp.TOTP(b32encode(str(otp_seed).encode()))
otp_value = str(otp.now())

print("OTP value is: " + otp_value)

print("Creating original PDF with OTP content")

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=100)
pdf.cell(200, 100, txt=otp_value, align="L")
pdf.output("out.pdf")

print("Creating tracking objects")
now = datetime.now()
tdm = TDM(Pattern4, content=dict(
    serial=324,
    hour=now.hour,
    minutes=now.minute,
    day=now.day,
    month=now.month,
    year=int(str(now.year)[2:]),
    manufacturer="Epson",
))
aa = AnonmaskApplierTdm(tdm, dotRadius=0.004)

print("Applying trackers")
with open("out_marked.pdf", 'wb') as pdfout:
    with open("out.pdf", "rb") as pdfin:
        pdfout.write(aa.apply(pdfin.read()))

print("Converting output PDF to PNG")
pages = pdf2image.convert_from_path("out_marked.pdf", 500)
pages[0].save('out_marked.png', 'PNG')

print("Finished")
