"""Ingestion pipeline runner.
Extracts, cleans, chunks health documents and produces an ingestion report.
"""
from pathlib import Path
import json
from collections import defaultdict
from typing import Dict, List, Any

from .cleaner import clean_health_text
from .chunker import chunk_document, DocumentChunk
from .curated_sources import OFFICIAL_HEALTH_DOCUMENTS


def run_ingestion(
    raw_dir: Path = Path("data/raw"),
    processed_dir: Path = Path("data/processed"),
    target_chunk_size: int = 250,
    chunk_overlap: int = 50,
) -> Dict[str, Any]:
    """Execute the end-to-end ingestion pipeline."""
    raw_dir.mkdir(parents=True, exist_ok=True)
    processed_dir.mkdir(parents=True, exist_ok=True)

    # 1. Populate raw documents
    for doc in OFFICIAL_HEALTH_DOCUMENTS:
        filename = f"{doc['doc_id']}_{doc['language']}.txt"
        file_path = raw_dir / filename
        file_path.write_text(doc["text"].strip(), encoding="utf-8")

    # 2. Extract, clean, and chunk
    all_chunks: List[DocumentChunk] = []
    stats: Dict[str, Any] = {
        "total_documents": len(OFFICIAL_HEALTH_DOCUMENTS),
        "chunks_per_language": defaultdict(int),
        "chunks_per_topic": defaultdict(int),
        "coverage_by_language_and_topic": defaultdict(lambda: defaultdict(int)),
        "total_chunks": 0,
    }

    for doc in OFFICIAL_HEALTH_DOCUMENTS:
        cleaned_text = clean_health_text(doc["text"])
        chunks = chunk_document(
            doc_id=doc["doc_id"],
            title=doc["title"],
            text=cleaned_text,
            language=doc["language"],
            topic=doc["topic"],
            url=doc["url"],
            section=doc["section"],
            target_chunk_size=target_chunk_size,
            chunk_overlap=chunk_overlap,
        )

        all_chunks.extend(chunks)
        stats["chunks_per_language"][doc["language"]] += len(chunks)
        stats["chunks_per_topic"][doc["topic"]] += len(chunks)
        stats["coverage_by_language_and_topic"][doc["language"]][doc["topic"]] += len(chunks)

    stats["total_chunks"] = len(all_chunks)

    # Convert defaultdicts for JSON serialization
    serialized_stats = {
        "total_documents": stats["total_documents"],
        "total_chunks": stats["total_chunks"],
        "chunks_per_language": dict(stats["chunks_per_language"]),
        "chunks_per_topic": dict(stats["chunks_per_topic"]),
        "coverage_by_language_and_topic": {
            lang: dict(topics)
            for lang, topics in stats["coverage_by_language_and_topic"].items()
        },
    }

    # 3. Save chunks and statistics
    output_chunks_file = processed_dir / "chunks.json"
    output_chunks_file.write_text(
        json.dumps([c.to_dict() for c in all_chunks], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    stats_file = processed_dir / "ingestion_report.json"
    stats_file.write_text(
        json.dumps(serialized_stats, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    # Print summary table
    print("=" * 60)
    print("INGESTION PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 60)
    print(f"Total documents processed: {stats['total_documents']}")
    print(f"Total chunks created:    {stats['total_chunks']}")
    print("-" * 60)
    print("Chunks per language:")
    for lang, count in stats["chunks_per_language"].items():
        print(f"  - {lang:5s}: {count:3d} chunks")
    print("-" * 60)
    print("Topic Coverage:")
    for topic, count in stats["chunks_per_topic"].items():
        print(f"  - {topic:45s}: {count} chunks")
    print("=" * 60)
    print(f"Artifacts saved to: {output_chunks_file} & {stats_file}")

    return serialized_stats


if __name__ == "__main__":
    run_ingestion()
