"""Text cleaning and normalization module for multilingual health documents."""
import re
import unicodedata


def clean_health_text(text: str) -> str:
    """
    Clean, normalize, and sanitize raw extracted health text.
    Preserves Indic characters, diacritics, and punctuation (e.g. Hindi/Odia purna viram)।
    """
    if not text:
        return ""

    # Normalize unicode to NFC for stable Indic script representations
    normalized = unicodedata.normalize("NFC", text)

    # Replace weird whitespace characters, zero-width spaces except ZWJ/ZWNJ if needed
    # Remove control characters except standard line breaks and tabs
    cleaned = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]", " ", normalized)

    # Collapse carriage returns
    cleaned = cleaned.replace("\r\n", "\n").replace("\r", "\n")

    # Remove repeated hyphens or underscores (line dividers)
    cleaned = re.sub(r"[-_]{3,}", " ", cleaned)

    # Replace multiple spaces/tabs within a line with a single space
    lines = []
    for line in cleaned.split("\n"):
        line = re.sub(r"[ \t]+", " ", line).strip()
        if line:
            lines.append(line)

    # Join lines with newlines, collapsing 3+ newlines into at most 2
    result = "\n".join(lines)
    result = re.sub(r"\n{3,}", "\n\n", result)
    return result.strip()
