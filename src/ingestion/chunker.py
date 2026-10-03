"""Chunking module with metadata preservation and sentence-boundary awareness."""
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional
import re


@dataclass
class DocumentChunk:
    chunk_id: str
    source_id: str
    title: str
    language: str
    topic: str
    url: str
    section: str
    text: str
    token_count: int

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def split_into_sentences(text: str) -> List[str]:
    """Split text into sentences respecting English and Indic punctuation (। and ॥)."""
    # Pattern matches period, exclamation, question mark, or Indic danda
    sentence_pattern = r"(?<=[.!?।॥\n])\s+"
    raw_sentences = re.split(sentence_pattern, text)
    sentences = [s.strip() for s in raw_sentences if s.strip()]
    return sentences if sentences else [text]


def approximate_token_count(text: str) -> int:
    """Approximate tokens based on whitespace and punctuation splits."""
    return len(re.findall(r"\w+|[^\w\s]", text, re.UNICODE))


def chunk_document(
    doc_id: str,
    title: str,
    text: str,
    language: str,
    topic: str,
    url: str,
    section: str = "General",
    target_chunk_size: int = 250,
    chunk_overlap: int = 50,
) -> List[DocumentChunk]:
    """
    Split a document into overlapping chunks of approx target_chunk_size tokens.
    Preserves sentence boundaries.
    """
    sentences = split_into_sentences(text)
    chunks: List[DocumentChunk] = []

    current_sentences: List[str] = []
    current_tokens = 0
    chunk_seq = 1

    for sent in sentences:
        sent_tokens = approximate_token_count(sent)
        if current_tokens + sent_tokens > target_chunk_size and current_sentences:
            chunk_text = " ".join(current_sentences).strip()
            chunk_id = f"{doc_id}_c{chunk_seq:03d}"
            chunks.append(
                DocumentChunk(
                    chunk_id=chunk_id,
                    source_id=doc_id,
                    title=title,
                    language=language,
                    topic=topic,
                    url=url,
                    section=section,
                    text=chunk_text,
                    token_count=approximate_token_count(chunk_text),
                )
            )
            chunk_seq += 1

            # Retain overlap sentences
            overlap_sentences: List[str] = []
            overlap_tokens = 0
            for prev_sent in reversed(current_sentences):
                p_tokens = approximate_token_count(prev_sent)
                if overlap_tokens + p_tokens <= chunk_overlap:
                    overlap_sentences.insert(0, prev_sent)
                    overlap_tokens += p_tokens
                else:
                    break

            current_sentences = overlap_sentences
            current_tokens = overlap_tokens

        current_sentences.append(sent)
        current_tokens += sent_tokens

    # Final chunk
    if current_sentences:
        chunk_text = " ".join(current_sentences).strip()
        chunk_id = f"{doc_id}_c{chunk_seq:03d}"
        chunks.append(
            DocumentChunk(
                chunk_id=chunk_id,
                source_id=doc_id,
                title=title,
                language=language,
                topic=topic,
                url=url,
                section=section,
                text=chunk_text,
                token_count=approximate_token_count(chunk_text),
            )
        )

    return chunks
