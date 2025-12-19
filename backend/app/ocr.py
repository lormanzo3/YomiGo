"""
OCR module using manga-ocr for Japanese text extraction.

manga-ocr is a machine learning model specifically trained on manga/anime
Japanese text, which makes it much more accurate than general-purpose OCR
(like Tesseract) for this use case. It handles:
- Vertical and horizontal text
- Stylized manga fonts
- Text on complex backgrounds
- Furigana (small reading hints above kanji)

The model runs locally - no internet required after initial download.
First run will download the model (~400MB) which may take a few minutes.
"""

import base64
import io
from PIL import Image

# manga_ocr import is deferred to avoid slow startup
# The model loads on first use
_mocr_instance = None


def get_ocr_instance():
    """
    Lazy-load the manga-ocr model.

    We defer loading because:
    1. The model takes 2-5 seconds to initialize
    2. We don't want to slow down server startup
    3. Memory is only used when OCR is actually needed

    The instance is cached globally so subsequent calls are instant.
    """
    global _mocr_instance
    if _mocr_instance is None:
        from manga_ocr import MangaOcr
        print("Loading manga-ocr model (first time may take a moment)...")
        _mocr_instance = MangaOcr()
        print("manga-ocr model loaded successfully!")
    return _mocr_instance


def extract_text_from_image(image_data: str) -> str:
    """
    Extract Japanese text from a base64-encoded image.

    Args:
        image_data: Base64 string of the image. Can include or exclude
                   the data URL prefix (data:image/png;base64,...)

    Returns:
        Extracted Japanese text as a string.

    Process:
    1. Decode base64 string to bytes
    2. Open as PIL Image
    3. Pass to manga-ocr model
    4. Return extracted text

    Example:
        >>> text = extract_text_from_image("iVBORw0KGgo...")
        >>> print(text)
        "今日は学校に行きました"
    """
    # Remove data URL prefix if present
    # Browser's canvas.toDataURL() includes "data:image/png;base64,"
    if "," in image_data:
        image_data = image_data.split(",")[1]

    # Decode base64 to bytes
    image_bytes = base64.b64decode(image_data)

    # Open as PIL Image (manga-ocr expects PIL Image or file path)
    image = Image.open(io.BytesIO(image_bytes))

    # Get OCR instance and extract text
    mocr = get_ocr_instance()
    text = mocr(image)

    return text


def is_ocr_available() -> bool:
    """
    Check if manga-ocr is available without loading the model.

    Used for health checks to verify the dependency is installed.
    """
    try:
        import manga_ocr
        return True
    except ImportError:
        return False
