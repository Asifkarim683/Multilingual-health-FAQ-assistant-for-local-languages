"""Text extraction utility supporting PDF, HTML, Markdown, and Text files."""
from pathlib import Path
from typing import Optional
import re
from bs4 import BeautifulSoup
from pypdf import PdfReader


def extract_text_from_pdf(file_path: Path) -> str:
    """Extract text page-by-page from a PDF document."""
    reader = PdfReader(str(file_path))
    pages_text = []
    for idx, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        if text.strip():
            pages_text.append(f"[Page {idx + 1}]\n{text}")
    return "\n\n".join(pages_text)


def extract_text_from_html(content: str) -> str:
    """Extract clean readable text from HTML, removing scripts, styles, and navigation."""
    soup = BeautifulSoup(content, "html.parser")
    # Remove unwanted tags
    for tag in soup(["script", "style", "nav", "footer", "header", "aside", "noscript"]):
        tag.decompose()

    # Get text
    text = soup.get_text(separator="\n")
    return text


def extract_text_from_file(file_path: Path) -> str:
    """Extract raw text from a given file path based on suffix."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    suffix = path.suffix.lower()
    if suffix == ".pdf":
        return extract_text_from_pdf(path)
    elif suffix in [".html", ".htm"]:
        raw_html = path.read_text(encoding="utf-8", errors="replace")
        return extract_text_from_html(raw_html)
    elif suffix in [".txt", ".md", ".json"]:
        return path.read_text(encoding="utf-8", errors="replace")
    else:
        # Fallback to plain text read
        return path.read_text(encoding="utf-8", errors="replace")
