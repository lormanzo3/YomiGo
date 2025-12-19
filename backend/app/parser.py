"""
Japanese morphological analysis using fugashi (MeCab wrapper).

Morphological analysis breaks Japanese text into individual tokens (words,
particles, conjugations) and identifies their grammatical properties.

Why this is essential for Japanese:
- Japanese has no spaces between words
- Words change form based on tense/politeness (conjugation)
- Need to identify the dictionary form to look up meanings

Example:
    "食べました" (I ate) breaks down to:
    - 食べ (stem of 食べる "to eat")
    - まし (polite auxiliary)
    - た (past tense marker)

We use fugashi + unidic-lite because:
- fugashi is a modern Python wrapper for MeCab (the standard tokenizer)
- unidic-lite provides a good dictionary with less disk space (~50MB vs 1GB+)
- Everything runs offline after installation
"""

from typing import Optional

# Deferred import for lazy loading
_tagger_instance = None

# Mapping Japanese POS tags to English
POS_MAPPING = {
    "名詞": "Noun",
    "動詞": "Verb",
    "形容詞": "Adjective",
    "副詞": "Adverb",
    "助詞": "Particle",
    "助動詞": "Auxiliary",
    "接続詞": "Conjunction",
    "感動詞": "Interjection",
    "連体詞": "Pre-noun adjectival",
    "接頭辞": "Prefix",
    "接尾辞": "Suffix",
    "記号": "Symbol",
    "補助記号": "Punctuation",
    "空白": "Whitespace",
}


def get_tagger():
    """
    Lazy-load the MeCab tagger with unidic-lite dictionary.

    The tagger is cached globally for performance.
    """
    global _tagger_instance
    if _tagger_instance is None:
        import fugashi
        _tagger_instance = fugashi.Tagger()
        print("MeCab tagger initialized with unidic-lite")
    return _tagger_instance


def parse_japanese_text(text: str) -> list[dict]:
    """
    Parse Japanese text into tokens with grammatical information.

    Args:
        text: Japanese text string to parse

    Returns:
        List of token dictionaries, each containing:
        - surface: The text as it appears
        - base_form: Dictionary form (lemma)
        - reading: Pronunciation in katakana
        - pos: Part of speech in Japanese
        - pos_english: Part of speech in English

    Example:
        >>> tokens = parse_japanese_text("日本語を勉強しています")
        >>> for t in tokens:
        ...     print(f"{t['surface']} -> {t['base_form']} ({t['pos_english']})")
        日本 -> 日本 (Noun)
        語 -> 語 (Noun)
        を -> を (Particle)
        勉強 -> 勉強 (Noun)
        し -> する (Verb)
        て -> て (Particle)
        い -> いる (Verb)
        ます -> ます (Auxiliary)
    """
    tagger = get_tagger()
    tokens = []

    for word in tagger(text):
        # Skip empty tokens
        if not word.surface:
            continue

        # Extract features from the UniDic analysis
        # UniDic provides rich morphological information
        pos = word.pos.split(",")[0] if word.pos else "不明"

        # Get the dictionary form (lemma) - fall back to surface if not available
        base_form = word.feature.lemma if word.feature.lemma else word.surface

        # Get reading in katakana
        reading = word.feature.kana if word.feature.kana else ""

        tokens.append({
            "surface": word.surface,
            "base_form": base_form,
            "reading": reading,
            "pos": pos,
            "pos_english": POS_MAPPING.get(pos, pos),
        })

    return tokens


def is_parser_available() -> bool:
    """
    Check if fugashi and unidic-lite are available.

    Used for health checks.
    """
    try:
        import fugashi
        return True
    except ImportError:
        return False
