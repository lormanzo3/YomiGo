"""
Japanese dictionary lookup using jamdict (JMdict wrapper).

JMdict is the primary free Japanese-English dictionary, containing:
- ~180,000 entries
- Multiple readings per entry
- Multiple meanings with usage notes
- Part of speech classifications
- This is the same data source that Jisho.org uses!

jamdict provides:
- Easy Python interface to JMdict
- Automatic download and caching of dictionary data
- SQLite-based storage for fast lookups
- Offline operation after initial setup

First run will download the dictionary data (~50MB compressed).
"""

from typing import Optional
from .models import DictionaryEntry

# Deferred import for lazy loading
_jamdict_instance = None


def get_jamdict():
    """
    Lazy-load the jamdict dictionary instance.

    On first call, this may download dictionary data if not present.
    The instance is cached for subsequent lookups.
    """
    global _jamdict_instance
    if _jamdict_instance is None:
        from jamdict import Jamdict
        print("Loading JMdict dictionary...")
        _jamdict_instance = Jamdict()
        print("JMdict dictionary loaded!")
    return _jamdict_instance


def lookup_word(word: str, reading: Optional[str] = None) -> list[DictionaryEntry]:
    """
    Look up a Japanese word in JMdict.

    Args:
        word: The word to look up (kanji, hiragana, or katakana)
        reading: Optional reading to filter results (useful for kanji with
                multiple readings)

    Returns:
        List of DictionaryEntry objects with definitions.
        Returns empty list if no matches found.

    Example:
        >>> entries = lookup_word("食べる")
        >>> print(entries[0].meanings)
        ['to eat']

        >>> entries = lookup_word("日", "ひ")  # Filter to "hi" reading
        >>> print(entries[0].meanings)
        ['sun', 'day', 'daytime']
    """
    jam = get_jamdict()

    # Look up the word - jamdict searches both kanji and kana forms
    result = jam.lookup(word)

    entries = []
    for entry in result.entries:
        # Extract kanji forms (or use kana if no kanji)
        kanji_forms = [k.text for k in entry.kanji_forms] if entry.kanji_forms else []
        kana_forms = [k.text for k in entry.kana_forms] if entry.kana_forms else []

        # Use first kanji form as the word, or first kana if no kanji
        entry_word = kanji_forms[0] if kanji_forms else (kana_forms[0] if kana_forms else word)
        entry_reading = kana_forms[0] if kana_forms else ""

        # If a specific reading was requested, filter to matching entries
        if reading and reading not in kana_forms:
            # Convert reading to hiragana for comparison if needed
            continue

        # Extract meanings from all senses
        meanings = []
        pos_tags = []
        for sense in entry.senses:
            # Get English glosses
            for gloss in sense.gloss:
                if gloss.lang in (None, "eng", "en"):  # English or unspecified
                    meanings.append(gloss.text)

            # Get part of speech tags
            for pos in sense.pos:
                if pos not in pos_tags:
                    pos_tags.append(pos)

        if meanings:  # Only include entries with English definitions
            entries.append(DictionaryEntry(
                word=entry_word,
                reading=entry_reading,
                meanings=meanings[:5],  # Limit to 5 meanings for UI
                part_of_speech=pos_tags[:3],  # Limit POS tags
            ))

    return entries


def lookup_tokens(tokens: list[dict]) -> list[dict]:
    """
    Add dictionary entries to a list of parsed tokens.

    Takes the output from parser.parse_japanese_text() and enriches
    each token with dictionary definitions.

    Args:
        tokens: List of token dicts from morphological analysis

    Returns:
        Same list with 'dictionary_entries' added to each token.

    Example:
        >>> tokens = parse_japanese_text("食べる")
        >>> enriched = lookup_tokens(tokens)
        >>> print(enriched[0]['dictionary_entries'][0]['meanings'])
        ['to eat']
    """
    for token in tokens:
        # Look up the base (dictionary) form, not the conjugated surface form
        # This ensures 食べました looks up 食べる, not 食べ
        base_form = token.get("base_form", token.get("surface", ""))

        # Skip particles and punctuation - they clutter results
        pos = token.get("pos", "")
        if pos in ("助詞", "補助記号", "記号", "空白"):
            token["dictionary_entries"] = []
            continue

        entries = lookup_word(base_form)

        # Convert to dict format for JSON serialization
        token["dictionary_entries"] = [
            {
                "word": e.word,
                "reading": e.reading,
                "meanings": e.meanings,
                "part_of_speech": e.part_of_speech,
            }
            for e in entries[:3]  # Limit to 3 entries per token
        ]

    return tokens


def is_dictionary_available() -> bool:
    """
    Check if jamdict is available.

    Used for health checks.
    """
    try:
        import jamdict
        return True
    except ImportError:
        return False
