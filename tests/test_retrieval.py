"""Unit tests for embedding generation, vector store search, and retrieval evaluation."""
import pytest
from pathlib import Path
from src.retrieval.embedder import MultilingualEmbedder, get_embedder
from src.retrieval.vector_store import VectorStore, SearchResult
from src.evaluation.eval_retrieval import evaluate_retrieval


def test_embedder_fit_and_embed():
    embedder = MultilingualEmbedder()
    corpus = [
        "Dengue causes high fever and joint pain.",
        "डेंगू बुखार के लक्षण तेज बुखार और सिरदर्द हैं।",
        "ଡେଙ୍ଗୁ ରୋଗର ଲକ୍ଷଣ ହେଉଛି ଜ୍ୱର।",
    ]
    embedder.fit(corpus)
    vecs = embedder.embed_texts(corpus)
    assert vecs.shape[0] == 3
    assert vecs.shape[1] > 0

    query_vec = embedder.embed_query("dengue symptoms")
    assert query_vec.shape[0] == vecs.shape[1]


def test_vector_store_search_confidence():
    chunks = [
        {
            "chunk_id": "SRC-01_c001",
            "source_id": "SRC-01",
            "title": "Dengue Guide",
            "language": "en",
            "topic": "Vector-borne diseases",
            "url": "https://who.int",
            "section": "Symptoms",
            "text": "Dengue fever warning signs include severe abdominal pain, persistent vomiting, and mucosal bleeding.",
            "token_count": 20,
        },
        {
            "chunk_id": "SRC-04_c001",
            "source_id": "SRC-04",
            "title": "Diabetes Guide",
            "language": "en",
            "topic": "Diabetes",
            "url": "https://who.int",
            "section": "General",
            "text": "Type 2 diabetes is linked with high blood sugar and insulin resistance. Exercise regularly.",
            "token_count": 20,
        }
    ]

    store = VectorStore()
    store.add_chunks(chunks)
    store.build_index()

    results = store.search("severe dengue abdominal pain", top_k=2)
    assert len(results) == 2
    assert results[0].chunk_id == "SRC-01_c001"
    assert results[0].score > results[1].score


def test_eval_retrieval_baseline():
    summary = evaluate_retrieval()
    assert summary["total_queries"] == 30
    assert summary["overall_recall_at_k"] >= 0.85
    assert summary["overall_mrr"] >= 0.70
    assert "en" in summary["per_language"]
    assert "hi" in summary["per_language"]
    assert "or" in summary["per_language"]
