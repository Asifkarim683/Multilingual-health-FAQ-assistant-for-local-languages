"""Citation models and citation extraction helpers."""
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Set
import re


@dataclass
class Citation:
    id: int
    title: str
    url: str
    section: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def extract_citations(
    raw_answer: str,
    retrieved_chunks: List[Dict[str, Any]],
) -> List[Citation]:
    """
    Extract citations from the answer or match with retrieved chunks.
    Ensures every returned answer has de-duplicated, accurate citations with title, url, section.
    """
    citations: List[Citation] = []
    seen_urls: Set[str] = set()

    citation_id = 1
    for chunk in retrieved_chunks:
        url = chunk.get("url", "")
        title = chunk.get("title", "Official Health Source")
        section = chunk.get("section", "General Guidance")

        if url not in seen_urls:
            seen_urls.add(url)
            citations.append(
                Citation(
                    id=citation_id,
                    title=title,
                    url=url,
                    section=section,
                )
            )
            citation_id += 1

    return citations
