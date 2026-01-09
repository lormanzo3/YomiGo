from manga_ocr import MangaOcr
from PIL import Image

mocr = MangaOcr()
img = Image.open("/mnt/c/Users/Mangc/OneDrive/Pictures/akira-japanese-vol-1-page-22-460_x2.jpg")  # <- Change this path!
text = mocr(img)
print('OCR Result:', text)
