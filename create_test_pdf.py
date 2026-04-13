from fpdf import FPDF
from PIL import Image, ImageDraw, ImageFont

# 1. Create an image containing text
img = Image.new('RGB', (400, 100), color = (255, 255, 255))
d = ImageDraw.Draw(img)
# Using default font
d.text((10, 10), "This is text inside an image.", fill=(0, 0, 0))
d.text((10, 30), "OCR should be able to read this.", fill=(0, 0, 0))
img.save('test_image.jpg')

# 2. Create PDF and insert the image
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)
pdf.cell(200, 10, txt="Hello World! This is regular text.", ln=1, align="C")

# Add a new page that ONLY contains the image so the text extractor will find no text
pdf.add_page()
pdf.image('test_image.jpg', x=10, y=10, w=100)

pdf.output("test_ocr.pdf")
