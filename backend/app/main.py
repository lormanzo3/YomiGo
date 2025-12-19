"""
YomiGo Backend - FastAPI server for Japanese manga OCR and dictionary lookup.

This server provides the core functionality for the YomiGo browser extension:
1. OCR: Extract Japanese text from manga page screenshots
2. Parse: Break down sentences into individual words/particles
3. Dictionary: Look up definitions for each word

The server runs locally on your machine, so:
- No internet required after initial setup
- Your reading data stays private
- Fast response times

Endpoints:
- POST /ocr      - Extract text from an image
- POST /parse    - Parse text and get dictionary definitions
- GET  /health   - Check if all services are working

Usage:
    cd backend
    pip install -r requirements.txt
    uvicorn app.main:app --reload --port 5000
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .models import OCRRequest, ParsedSentence, Token, HealthResponse
from .ocr import extract_text_from_image, is_ocr_available
from .parser import parse_japanese_text, is_parser_available
from .dictionary import lookup_tokens, is_dictionary_available


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Startup and shutdown events for the FastAPI application.

    On startup: Print welcome message and check dependencies
    On shutdown: Cleanup (if needed)
    """
    # Startup
    print("=" * 50)
    print("YomiGo Backend Starting...")
    print("=" * 50)
    print(f"OCR (manga-ocr):     {'Available' if is_ocr_available() else 'NOT INSTALLED'}")
    print(f"Parser (fugashi):     {'Available' if is_parser_available() else 'NOT INSTALLED'}")
    print(f"Dictionary (jamdict): {'Available' if is_dictionary_available() else 'NOT INSTALLED'}")
    print("=" * 50)
    print("Server ready! Extension can connect to http://localhost:5000")
    print("=" * 50)

    yield  # Server runs here

    # Shutdown
    print("YomiGo Backend shutting down...")


# Create FastAPI application
app = FastAPI(
    title="YomiGo API",
    description="Japanese manga OCR and dictionary lookup service",
    version="0.1.0",
    lifespan=lifespan,
)

# Configure CORS to allow requests from browser extension
# Extensions run from chrome-extension:// or moz-extension:// origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (needed for extensions)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint to verify all services are operational.

    Returns status of each component:
    - ocr: manga-ocr is installed and importable
    - parser: fugashi is installed and importable
    - dictionary: jamdict is installed and importable

    The extension can call this on startup to warn users if
    the backend isn't running or has missing dependencies.
    """
    return HealthResponse(
        status="healthy",
        services={
            "ocr": is_ocr_available(),
            "parser": is_parser_available(),
            "dictionary": is_dictionary_available(),
        }
    )


@app.post("/ocr")
async def perform_ocr(request: OCRRequest) -> dict:
    """
    Extract Japanese text from an image using manga-ocr.

    Request body:
        image_data: Base64-encoded image (PNG, JPG, etc.)
                   Can include data URL prefix or just the base64 string

    Returns:
        text: Extracted Japanese text

    Example:
        POST /ocr
        {"image_data": "data:image/png;base64,iVBORw0KGgo..."}

        Response:
        {"text": "今日は学校に行きました"}
    """
    try:
        text = extract_text_from_image(request.image_data)
        return {"text": text}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"OCR processing failed: {str(e)}"
        )


@app.post("/parse", response_model=ParsedSentence)
async def parse_text(request: OCRRequest) -> ParsedSentence:
    """
    Full pipeline: OCR -> Parse -> Dictionary lookup.

    This is the main endpoint used by the extension. It:
    1. Extracts text from the image using manga-ocr
    2. Parses the text into tokens using MeCab
    3. Looks up each token in JMdict
    4. Returns the complete breakdown

    Request body:
        image_data: Base64-encoded image

    Returns:
        original_text: The raw OCR'd text
        tokens: List of tokens, each with:
            - surface: Text as it appears
            - base_form: Dictionary form
            - reading: Pronunciation
            - pos: Part of speech (Japanese)
            - pos_english: Part of speech (English)
            - dictionary_entries: List of definitions

    Example response:
    {
        "original_text": "食べました",
        "tokens": [
            {
                "surface": "食べ",
                "base_form": "食べる",
                "reading": "タベ",
                "pos": "動詞",
                "pos_english": "Verb",
                "dictionary_entries": [
                    {
                        "word": "食べる",
                        "reading": "たべる",
                        "meanings": ["to eat"],
                        "part_of_speech": ["Ichidan verb"]
                    }
                ]
            },
            ...
        ]
    }
    """
    try:
        # Step 1: OCR - extract text from image
        text = extract_text_from_image(request.image_data)

        if not text:
            return ParsedSentence(original_text="", tokens=[])

        # Step 2: Parse - break into tokens with MeCab
        tokens = parse_japanese_text(text)

        # Step 3: Dictionary - look up each token
        enriched_tokens = lookup_tokens(tokens)

        # Convert to response model
        token_models = [
            Token(
                surface=t["surface"],
                base_form=t["base_form"],
                reading=t["reading"],
                pos=t["pos"],
                pos_english=t.get("pos_english"),
                dictionary_entries=t.get("dictionary_entries", []),
            )
            for t in enriched_tokens
        ]

        return ParsedSentence(
            original_text=text,
            tokens=token_models,
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Processing failed: {str(e)}"
        )


@app.post("/parse-text")
async def parse_text_only(text: str) -> ParsedSentence:
    """
    Parse pre-extracted text (skip OCR step).

    Useful for:
    - Testing the parser without an image
    - Re-parsing text that was already OCR'd
    - Parsing text from other sources (copied from web, etc.)

    Query parameter:
        text: Japanese text to parse

    Returns:
        Same format as /parse endpoint
    """
    try:
        if not text:
            return ParsedSentence(original_text="", tokens=[])

        tokens = parse_japanese_text(text)
        enriched_tokens = lookup_tokens(tokens)

        token_models = [
            Token(
                surface=t["surface"],
                base_form=t["base_form"],
                reading=t["reading"],
                pos=t["pos"],
                pos_english=t.get("pos_english"),
                dictionary_entries=t.get("dictionary_entries", []),
            )
            for t in enriched_tokens
        ]

        return ParsedSentence(
            original_text=text,
            tokens=token_models,
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Processing failed: {str(e)}"
        )


# Entry point for running directly with Python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
