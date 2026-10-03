"""Unit tests for text extraction, cleaning, and chunking."""
import pytest
from pathlib import Path
from src.ingestion.cleaner import clean_health_text
from src.ingestion.chunker import (
    chunk_document,
    split_into_sentences,
    approximate_token_count,
    DocumentChunk,
)
from src.ingestion.run import run_ingestion


def test_clean_health_text_whitespace_and_indic():
    raw = "  डेंगू   के मुख्य \t लक्षण: तेज बुखार।\r\n\r\n\r\nपानी खूब पिएं।  "
    cleaned = clean_health_text(raw)
    assert "डेंगू के मुख्य लक्षण: तेज बुखार।" in cleaned
    assert "पानी खूब पिएं।" in cleaned
    assert "\r" not in cleaned
    assert "\n\n\n" not in cleaned


def test_clean_health_text_odia():
    raw = "  ଓଡ଼ିଶାରେ   ଡେଙ୍ଗୁ ରୋଗର   ଚିକିତ୍ସା।  "
    cleaned = clean_health_text(raw)
    assert cleaned == "ଓଡ଼ିଶାରେ ଡେଙ୍ଗୁ ରୋଗର ଚିକିତ୍ସା।"


def test_split_into_sentences():
    # English sentences
    en_text = "Fever is common. Drink plenty of fluids! Seek medical help if symptoms worsen."
    en_sents = split_into_sentences(en_text)
    assert len(en_sents) == 3

    # Hindi sentences with danda
    hi_text = "डेंगू मच्छर से फैलता है। पानी जमा न होने दें। लक्षण दिखने पर जांच कराएं।"
    hi_sents = split_into_sentences(hi_text)
    assert len(hi_sents) == 3
    assert hi_sents[0] == "डेंगू मच्छर से फैलता है।"

    # Odia sentences with danda
    or_text = "ଡେଙ୍ଗୁ ଏକ ମଶାଜନିତ ରୋଗ। ଏଥିପାଇଁ ସତର୍କ ରୁହନ୍ତୁ।"
    or_sents = split_into_sentences(or_text)
    assert len(or_sents) == 2


def test_chunk_document_metadata_and_structure():
    doc_id = "TEST-01"
    title = "Test Guide"
    text = (
        "Dengue is transmitted by mosquitoes. Symptoms include high fever and severe headache. "
        "Drinking oral rehydration salts helps manage dehydration. "
        "Severe dengue requires emergency medical care at a hospital. "
        "Eliminate stagnant water containers once every week to prevent breeding."
    )
    chunks = chunk_document(
        doc_id=doc_id,
        title=title,
        text=text,
        language="en",
        topic="Vector-borne diseases",
        url="https://example.com/test",
        section="Symptoms",
        target_chunk_size=30,
        chunk_overlap=10,
    )

    assert len(chunks) >= 1
    first_chunk = chunks[0]
    assert isinstance(first_chunk, DocumentChunk)
    assert first_chunk.source_id == doc_id
    assert first_chunk.language == "en"
    assert first_chunk.topic == "Vector-borne diseases"
    assert first_chunk.url == "https://example.com/test"
    assert first_chunk.token_count > 0


def test_run_ingestion_end_to_end(tmp_path):
    raw_dir = tmp_path / "raw"
    processed_dir = tmp_path / "processed"

    stats = run_ingestion(raw_dir=raw_dir, processed_dir=processed_dir)

    assert stats["total_documents"] == 24
    assert stats["total_chunks"] >= 24
    assert "en" in stats["chunks_per_language"]
    assert "hi" in stats["chunks_per_language"]
    assert "or" in stats["chunks_per_language"]

    # Verify output files
    assert (processed_dir / "chunks.json").exists()
    assert (processed_dir / "ingestion_report.json").exists()
