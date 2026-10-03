"""Vector store implementation for cosine similarity retrieval across multilingual chunks."""
from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Union
from pathlib import Path
import json
import pickle
import numpy as np

from .embedder import get_embedder, MultilingualEmbedder


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
    """In-memory vector store with persistence and cosine similarity search."""

    def __init__(self, embedder: Optional[MultilingualEmbedder] = None):
        self.embedder = embedder or get_embedder()
        self.chunks: List[Dict[str, Any]] = []
        self.embeddings: Optional[np.ndarray] = None

    def add_chunks(self, chunks: List[Dict[str, Any]]):
        """Add chunks to the vector store."""
        self.chunks.extend(chunks)

    def build_index(self):
        """Compute embeddings for all stored chunks."""
        if not self.chunks:
            raise ValueError("No chunks to index.")
        texts = [c["text"] for c in self.chunks]
        self.embedder.fit(texts)
        self.embeddings = self.embedder.embed_texts(texts)

    def search(
        self,
        query: str,
        top_k: int = 5,
        lang_filter: Optional[str] = None,
    ) -> List[SearchResult]:
        """
        Search for top_k relevant chunks using cosine similarity.
        Optionally filter by target language.
        """
        if self.embeddings is None or not self.chunks:
            raise ValueError("Vector store is empty or unindexed. Call build_index() first.")

        query_vec = self.embedder.embed_query(query)
        # Cosine similarity since vectors are L2-normalized
        scores = np.dot(self.embeddings, query_vec)

        # Sort indices by score descending
        sorted_indices = np.argsort(scores)[::-1]

        results: List[SearchResult] = []
        rank = 1
        for idx in sorted_indices:
            chunk = self.chunks[idx]
            if lang_filter and chunk.get("language") != lang_filter:
                continue

            score = float(scores[idx])
            results.append(
                SearchResult(
                    chunk_id=chunk["chunk_id"],
                    source_id=chunk["source_id"],
                    title=chunk["title"],
                    language=chunk["language"],
                    topic=chunk["topic"],
                    url=chunk["url"],
                    section=chunk["section"],
                    text=chunk["text"],
                    score=score,
                    rank=rank,
                )
            )
            rank += 1
            if len(results) >= top_k:
                break

        return results

    def save(self, directory: Union[str, Path]):
        """Persist index, chunks, and embedder to directory."""
        dir_path = Path(directory)
        dir_path.mkdir(parents=True, exist_ok=True)

        with open(dir_path / "chunks.json", "w", encoding="utf-8") as f:
            json.dump(self.chunks, f, ensure_ascii=False, indent=2)

        if self.embeddings is not None:
            np.save(dir_path / "embeddings.npy", self.embeddings)

        self.embedder.save(dir_path / "embedder.pkl")

    @classmethod
    def load(cls, directory: Union[str, Path]) -> "VectorStore":
        """Load vector store from saved directory."""
        dir_path = Path(directory)
        store = cls()

        with open(dir_path / "chunks.json", "r", encoding="utf-8") as f:
            store.chunks = json.load(f)

        if (dir_path / "embeddings.npy").exists():
            store.embeddings = np.load(dir_path / "embeddings.npy")

        if (dir_path / "embedder.pkl").exists():
            store.embedder.load(dir_path / "embedder.pkl")

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
