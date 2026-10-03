"""Vector store implementation for hybrid (dense + sparse BM25) and cosine similarity retrieval across multilingual chunks."""
from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Union
from pathlib import Path
import json
import pickle
import numpy as np

from .embedder import get_embedder, MultilingualEmbedder
from .bm25 import BM25Index, reciprocal_rank_fusion


@dataclass
class SearchResult:
    chunk_id: str
    source_id: str
    title: str
    language: str
    topic: str
    url: str
    section: str
    text: str
    score: float
    rank: int

    def to_dict(self) -> Dict[str, Any]:
        return {
            "chunk_id": self.chunk_id,
            "source_id": self.source_id,
            "title": self.title,
            "language": self.language,
            "topic": self.topic,
            "url": self.url,
            "section": self.section,
            "text": self.text,
            "score": round(float(self.score), 4),
            "rank": self.rank,
        }


class VectorStore:
    """
    Multilingual Vector Store supporting hybrid retrieval (Dense Semantic Cosine + Sparse BM25),
    pure dense cosine similarity, pure sparse BM25, and Reciprocal Rank Fusion (RRF).
    """

    def __init__(
        self,
        embedder: Optional[MultilingualEmbedder] = None,
        bm25: Optional[BM25Index] = None,
    ):
        self.embedder = embedder or get_embedder()
        self.bm25: Optional[BM25Index] = bm25
        self.chunks: List[Dict[str, Any]] = []
        self.embeddings: Optional[np.ndarray] = None

    def add_chunks(self, chunks: List[Dict[str, Any]]):
        """Add chunks to the vector store."""
        self.chunks.extend(chunks)

    def build_index(self):
        """Compute embeddings and BM25 sparse index for all stored chunks."""
        if not self.chunks:
            raise ValueError("No chunks to index.")
        texts = [c["text"] for c in self.chunks]
        self.embedder.fit(texts)
        self.embeddings = self.embedder.embed_texts(texts)
        self.bm25 = BM25Index()
        self.bm25.fit(texts)

    def search(
        self,
        query: str,
        top_k: int = 5,
        lang_filter: Optional[str] = None,
        mode: str = "hybrid",
        alpha: float = 0.65,
    ) -> List[SearchResult]:
        """
        Search for top_k relevant chunks.
        Modes:
            - "hybrid": Calibrated combination of dense cosine similarity and sparse BM25 keyword matching (default).
            - "dense": Pure semantic embedding cosine similarity.
            - "sparse": Pure Okapi BM25 lexical keyword matching.
            - "rrf": Reciprocal Rank Fusion of dense and sparse rankings.
        Prioritizes chunks matching lang_filter, falling back to cross-lingual chunks.
        """
        if self.embeddings is None or not self.chunks:
            raise ValueError("Vector store is empty or unindexed. Call build_index() first.")

        query_vec = self.embedder.embed_query(query)
        dense_scores = np.dot(self.embeddings, query_vec)

        # Lazy initialize BM25 if needed
        if self.bm25 is None and mode in ("hybrid", "sparse", "rrf"):
            self.bm25 = BM25Index()
            self.bm25.fit([c["text"] for c in self.chunks])

        if mode == "dense":
            scores = dense_scores
            sorted_indices = np.argsort(scores)[::-1]
        elif mode == "sparse":
            scores = self.bm25.get_scores(query)
            sorted_indices = np.argsort(scores)[::-1]
        elif mode == "rrf":
            sparse_scores = self.bm25.get_scores(query)
            dense_ranks = np.argsort(dense_scores)[::-1].tolist()
            sparse_ranks = np.argsort(sparse_scores)[::-1].tolist()
            rrf_map = reciprocal_rank_fusion(
                dense_ranks, sparse_ranks, sparse_scores=sparse_scores, k=60, w_dense=0.6, w_sparse=0.4
            )
            sorted_indices = sorted(range(len(self.chunks)), key=lambda idx: rrf_map[idx], reverse=True)
            boost = 1.0 + 0.35 * (sparse_scores / (sparse_scores + 15.0))
            scores = dense_scores * boost
        elif mode == "hybrid":
            sparse_scores = self.bm25.get_scores(query)
            # Semantically grounded BM25 keyword boost:
            # Gated by semantic similarity so out-of-scope queries (dense < 0.15) cannot bypass refusal thresholds
            boost = 1.0 + 0.35 * (sparse_scores / (sparse_scores + 15.0))
            scores = dense_scores * boost
            sorted_indices = np.argsort(scores)[::-1]
        else:
            raise ValueError(f"Unknown search mode: {mode}. Choose from 'hybrid', 'dense', 'sparse', 'rrf'.")

        matching_results: List[SearchResult] = []
        fallback_results: List[SearchResult] = []

        for idx in sorted_indices:
            chunk = self.chunks[idx]
            score = float(scores[idx])
            res = SearchResult(
                chunk_id=chunk["chunk_id"],
                source_id=chunk["source_id"],
                title=chunk["title"],
                language=chunk["language"],
                topic=chunk["topic"],
                url=chunk["url"],
                section=chunk["section"],
                text=chunk["text"],
                score=score,
                rank=0,
            )
            if lang_filter:
                if chunk.get("language") == lang_filter:
                    matching_results.append(res)
                else:
                    fallback_results.append(res)
            else:
                matching_results.append(res)

        combined = (matching_results[:top_k] + fallback_results)[:top_k]
        for rank, r in enumerate(combined, 1):
            r.rank = rank

        return combined

    def save(self, directory: Union[str, Path]):
        """Persist index, chunks, embedder, and BM25 index to directory."""
        dir_path = Path(directory)
        dir_path.mkdir(parents=True, exist_ok=True)

        with open(dir_path / "chunks.json", "w", encoding="utf-8") as f:
            json.dump(self.chunks, f, ensure_ascii=False, indent=2)

        if self.embeddings is not None:
            np.save(dir_path / "embeddings.npy", self.embeddings)

        self.embedder.save(dir_path / "embedder.pkl")

        if self.bm25 is not None:
            self.bm25.save(dir_path / "bm25.pkl")

    @classmethod
    def load(cls, directory: Union[str, Path]) -> "VectorStore":
        """Load vector store from saved directory with backwards compatibility."""
        dir_path = Path(directory)
        store = cls()

        with open(dir_path / "chunks.json", "r", encoding="utf-8") as f:
            store.chunks = json.load(f)

        if (dir_path / "embeddings.npy").exists():
            store.embeddings = np.load(dir_path / "embeddings.npy")

        if (dir_path / "embedder.pkl").exists():
            store.embedder.load(dir_path / "embedder.pkl")

        if (dir_path / "bm25.pkl").exists():
            store.bm25 = BM25Index.load(dir_path / "bm25.pkl")
        elif store.chunks:
            # Backwards compatibility: automatically fit BM25 on loaded chunks
            store.bm25 = BM25Index()
            store.bm25.fit([c["text"] for c in store.chunks])

        return store

    @classmethod
    def from_processed_chunks(
        cls, chunks_path: Union[str, Path] = "data/processed/chunks.json"
    ) -> "VectorStore":
        """Create and index a vector store from processed chunks file."""
        path = Path(chunks_path)
        if not path.exists():
            raise FileNotFoundError(f"Chunks file not found at {path}. Run ingestion first.")

        with open(path, "r", encoding="utf-8") as f:
            chunks_data = json.load(f)

        store = cls()
        store.add_chunks(chunks_data)
        store.build_index()
        return store
