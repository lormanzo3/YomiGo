"""
Pydantic models for API request/response validation.

These models define the data structures used throughout the application:
- OCRRequest: Image data sent from the browser extension
- Token: A single parsed Japanese word/particle with dictionary info
- ParsedSentence: Complete sentence breakdown with all tokens
- DictionaryEntry: Full dictionary entry for a word
"""

from pydantic import BaseModel
from typing import Optional


class OCRRequest(BaseModel):
    """
    Request model for OCR processing.

    The browser extension captures a screenshot or selection of the manga page
    and sends it as a base64-encoded image string.
    """
    image_data: str  # Base64 encoded image from the browser extension


class DictionaryEntry(BaseModel):
    """
    A single dictionary entry from JMdict.

    JMdict entries contain:
    - word: The word in kanji (if applicable)
    - reading: Hiragana/katakana reading
    - meanings: List of English definitions
    - part_of_speech: Grammatical classification (noun, verb, etc.)
    """
    word: str
    reading: str
    meanings: list[str]
    part_of_speech: list[str]


class Token(BaseModel):
    """
    A single token (word/particle) from morphological analysis.

    MeCab breaks Japanese sentences into tokens, where each token is:
    - surface: The exact text as it appears in the sentence
    - base_form: Dictionary form (e.g., 食べた -> 食べる)
    - reading: How to pronounce it (in katakana from MeCab)
    - pos: Part of speech (名詞, 動詞, 助詞, etc.)
    - dictionary_entries: Matching entries from JMdict (if found)

    Example: "食べました" breaks into:
    - Token(surface="食べ", base_form="食べる", pos="動詞")
    - Token(surface="まし", base_form="ます", pos="助動詞")
    - Token(surface="た", base_form="た", pos="助動詞")
    """
    surface: str  # The actual text as it appears
    base_form: str  # Dictionary form of the word
    reading: str  # Pronunciation in kana
    pos: str  # Part of speech (Japanese)
    pos_english: Optional[str] = None  # Part of speech (English)
    dictionary_entries: list[DictionaryEntry] = []


class ParsedSentence(BaseModel):
    """
    Complete response from the /parse endpoint.

    Contains the original OCR'd text and its full breakdown into tokens,
    similar to how Jisho.org displays sentence analysis.
    """
    original_text: str  # Raw text extracted by OCR
    tokens: list[Token]  # List of parsed tokens with dictionary info


class HealthResponse(BaseModel):
    """Health check response model."""
    status: str
    services: dict[str, bool]
