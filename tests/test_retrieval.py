"""Unit tests for embedding generation, vector store search, BM25 keyword search, and retrieval evaluation."""
import pytest
from pathlib import Path
import tempfile
import numpy as np

from src.retrieval.embedder import MultilingualEmbedder, get_embedder
from src.retrieval.bm25 import BM25Index, tokenize_multilingual, reciprocal_rank_fusion
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


def test_bm25_multilingual_indexing_and_scoring():
    corpus = [
        "Oral rehydration salts ORS preparation with 1000 mL water.",
        "डेंगू बुखार और तेज सिरदर्द के लक्षण।",
        "ଡେଙ୍ଗୁ ଜ୍ୱରରେ ପାରାସିଟାମୋଲ ଏବଂ ପ୍ରଚୁର ପାଣି ପିଅନ୍ତୁ।",
    ]
    bm25 = BM25Index()
    bm25.fit(corpus)
    assert bm25.corpus_size == 3

    # Exact token query in English
    scores_en = bm25.get_scores("ORS preparation")
    assert scores_en[0] > scores_en[1]
    assert scores_en[0] > scores_en[2]

    # Exact token query in Hindi
    scores_hi = bm25.get_scores("सिरदर्द")
    assert scores_hi[1] > scores_hi[0]

    # Exact token query in Odia
    scores_or = bm25.get_scores("ପାରାସିଟାମୋଲ")
    assert scores_or[2] > scores_or[0]


def test_bm25_save_and_load():
    corpus = [
        "Type 2 diabetes insulin management.",
        "डायबिटीज में ब्लड शुगर का नियंत्रण।",
    ]
    bm25 = BM25Index()
    bm25.fit(corpus)

    with tempfile.TemporaryDirectory() as tmpdir:
        save_path = Path(tmpdir) / "bm25.pkl"
        bm25.save(save_path)
        assert save_path.exists()

        loaded_bm25 = BM25Index.load(save_path)
        assert loaded_bm25.corpus_size == 2
        orig_scores = bm25.get_scores("insulin")
        loaded_scores = loaded_bm25.get_scores("insulin")
        np.testing.assert_allclose(orig_scores, loaded_scores)


def test_reciprocal_rank_fusion():
    dense_ranks = [0, 1, 2, 3]
    sparse_ranks = [1, 0, 3, 2]
    sparse_scores = np.array([5.0, 8.0, 0.0, 2.0])

    rrf = reciprocal_rank_fusion(dense_ranks, sparse_ranks, sparse_scores=sparse_scores, k=60)
    # Doc 0 is rank 1 in dense, rank 2 in sparse -> high RRF
    # Doc 1 is rank 2 in dense, rank 1 in sparse -> high RRF
    assert rrf[0] > rrf[3]
    assert rrf[1] > rrf[3]
    # Doc 2 has sparse_score == 0 so receives no sparse rank boost
    assert rrf[2] < rrf[0]


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

    # Test hybrid mode (default)
    results = store.search("severe dengue abdominal pain", top_k=2, mode="hybrid")
    assert len(results) == 2
    assert results[0].chunk_id == "SRC-01_c001"
    assert results[0].score > results[1].score

    # Test pure dense mode
    res_dense = store.search("severe dengue abdominal pain", top_k=2, mode="dense")
    assert res_dense[0].chunk_id == "SRC-01_c001"

    # Test pure sparse mode
    res_sparse = store.search("severe dengue abdominal pain", top_k=2, mode="sparse")
    assert res_sparse[0].chunk_id == "SRC-01_c001"

    # Test RRF mode
    res_rrf = store.search("severe dengue abdominal pain", top_k=2, mode="rrf")
    assert res_rrf[0].chunk_id == "SRC-01_c001"


def test_eval_retrieval_baseline():
    summary = evaluate_retrieval()
    assert summary["total_queries"] == 30
    assert summary["overall_recall_at_k"] >= 0.85
    assert summary["overall_mrr"] >= 0.70
    assert "en" in summary["per_language"]
    assert "hi" in summary["per_language"]
    assert "or" in summary["per_language"]
