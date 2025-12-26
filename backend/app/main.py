from fastapi import FastAPI, File, UploadFile
from manga_ocr import MangaOcr
from PIL import Image
from fugashi import Tagger
from jamdict import Jamdict
import io

def katakana_to_hiragana(text):
      """Convert katakana to hiragana."""
      result = ""
      for char in text:
          code = ord(char)
          # Katakana range: 0x30A1 (ァ) to 0x30F6 (ヶ)
          if 0x30A1 <= code <= 0x30F6:
              # Shift to hiragana range (0x3041 to 0x3096)
              result += chr(code - 0x60)
          else:
              result += char
      return result

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
        pos = word.pos  # Part of speech, like "助詞,接続助詞,*,*"

        # check if it's a particle or auxiliary verb (grammar words)
        if pos.startswith("助詞") or pos.startswith("助動詞"):
            # Skip dictionary lookup for grammar words
            results.append({
                "surface": str(word),
                "reading": katakana_to_hiragana(word.feature.kana or ""),
                "dictionary_form": dictionary_form,
                "part_of_speech": pos,
                "definitions": ["(grammatical particle)"]
            })
            continue # Skip to next word

        # For regular words, look up the word
        lookup = jam.lookup(dictionary_form)

        definitions = []
        for entry in lookup.entries[:3]:
            for sense in entry.senses:
                definitions.append(", ".join(str(g) for g in sense.gloss))

        results.append({
            "surface": str(word), #How it appears in text
            "reading": katakana_to_hiragana(word.feature.kana or ""),
            "dictionary_form": dictionary_form, #Base form
            "part_of_speech": pos, #Noun, verb, etc.
            "definitions": definitions
        }) # Limit to 3 definitions

    return {"tokens": results}
