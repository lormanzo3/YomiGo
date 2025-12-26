from fastapi import FastAPI, File, UploadFile
from manga_ocr import MangaOcr
from PIL import Image
import io


app = FastAPI()
mocr = MangaOcr()

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/ocr")
async def extract_text(image: UploadFile = File(...)):
    contents = await image.read()
    img = Image.open(io.BytesIO(contents))
    text = mocr(img)
    return {"text": text}
