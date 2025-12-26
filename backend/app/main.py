from fastapi import FastAPI, File, UploadFile
from manga_ocr import MangaOcr
from PIL import Image
from fugashi import Tagger
from jamdict import Jamdict
import io


app = FastAPI()
mocr = MangaOcr()
tagger = Tagger()
jam = Jamdict()

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/ocr")
async def extract_text(image: UploadFile = File(...)):
    contents = await image.read()
    img = Image.open(io.BytesIO(contents))
    text = mocr(img)
    return {"text": text}

@app.post ("/parse")
async def parse_text(data: dict):
    text = data.get("text", "")

    results = []

    for word in tagger(text):
        # get the dictionary form of the word
        dictionary_form = word.feature.lemma or str(word)

        # look up the word
        lookup = jam.lookup(dictionary_form)

        definitions = []
        for entry in lookup.entries[:3]:
            for sense in entry.senses:
                definitions.append(", ".join(str(g) for g in sense.gloss))

        results.append({
            "surface": str(word), #How it appears in text
            "dictionary_form": dictionary_form, #Base form
            "part_of_speech": word.pos, #Noun, verb, etc.
            "definitions": definitions
        }) # Limit to 3 definitions

    return {"tokens": results}
