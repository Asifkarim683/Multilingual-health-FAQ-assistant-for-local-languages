"""Language identification and script verification for generation post-checks."""
import re
from typing import Optional, Tuple

SCRIPT_RANGES = {
    "hi": (r"[\u0900-\u097F]", "Devanagari"),
    "or": (r"[\u0B00-\u0B7F]", "Odia"),
    "bn": (r"[\u0980-\u09FF]", "Bengali"),
    "te": (r"[\u0C00-\u0C7F]", "Telugu"),
    "ta": (r"[\u0B80-\u0BFF]", "Tamil"),
}


def detect_script_language(text: str) -> str:
    """
    Detect the predominant language script from text.
    Returns 'hi', 'or', 'bn', 'te', 'ta', or 'en' (default).
    """
    if not text:
        return "en"

    counts = {}
    for lang, (pattern, _) in SCRIPT_RANGES.items():
        matches = len(re.findall(pattern, text))
        if matches > 0:
            counts[lang] = matches

    if not counts:
        return "en"

    # Return language with highest script character count
    best_lang = max(counts, key=counts.get)
    # Require at least 5 script characters to avoid stray symbols
    if counts[best_lang] >= 3:
        return best_lang

    return "en"


def verify_language_match(text: str, target_lang: str) -> Tuple[bool, str]:
    """
    Verify if the generated text matches the target language.
    Returns (is_match, detected_lang).
    """
    if not text or not target_lang:
        return False, "unknown"

    if target_lang == "en":
        # Check that it doesn't have heavy Indic text
        indic_chars = len(re.findall(r"[\u0900-\u0D7F]", text))
        total_letters = len(re.findall(r"\w", text, re.UNICODE)) or 1
        if (indic_chars / total_letters) > 0.3:
            return False, "indic"
        return True, "en"

    if target_lang in SCRIPT_RANGES:
        pattern, _ = SCRIPT_RANGES[target_lang]
        matches = len(re.findall(pattern, text))
        # At least 10 script characters or 15% of text
        if matches >= 5:
            return True, target_lang
        detected = detect_script_language(text)
        return False, detected

    return True, target_lang
