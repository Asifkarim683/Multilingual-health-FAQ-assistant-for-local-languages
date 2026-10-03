"""Embedder module supporting cross-lingual TF-IDF/Dense embeddings and Gemini API embeddings."""
import os
import re
import numpy as np
from typing import List, Optional, Union
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize
import pickle
from pathlib import Path


# Cross-lingual health term map bridging Indic health terms to core health concepts
CROSS_LINGUAL_HEALTH_SYNONYMS = {
    # Dengue / Vector
    "dengue": ["dengue", "डेंगू", "ଡେଙ୍ଗୁ", "aedes", "mosquito", "मच्छर", "ମଶା", "platelet"],
    "malaria": ["malaria", "मलेरिया", "ମ୍ୟାଲେରିଆ", "mosquito", "fever", "बुखार", "ଜ୍ୱର"],
    # Diabetes
    "diabetes": ["diabetes", "डायबिटीज", "ଡାଇବେଟିସ୍", "मधुमेह", "ମଧୁମେହ", "sugar", "शुगर", "ଶୁଗାର", "शर्करा", "ଶର୍କରା", "glucose", "insulin", "इंसुलिन"],
    # Hypertension / BP
    "hypertension": ["hypertension", "blood pressure", "ब्लड प्रेशर", "ବ୍ଲଡ ପ୍ରେସର", "रक्तचाप", "ରକ୍ତଚାପ", "हाई बीपी", "ହାଇ ବିପି", "salt", "नमक", "ଲୁଣ"],
    # Immunization
    "vaccine": ["vaccine", "immunization", "टीका", "टीकाकरण", "ଟିକା", "ଟୀକାକରଣ", "bcg", "polio", "पोलियो", "ପୋଲିଓ", "pentavalent", "पेंटावेलेंट", "ପେଣ୍ଟାଭାଲେଣ୍ଟ", "schedule"],
    # Maternal
    "maternal": ["maternal", "pregnancy", "pregnant", "गर्भावस्था", "गर्भवती", "ଗର୍ଭାବସ୍ଥା", "ଗର୍ଭବତୀ", "anc", "pmsma", "trimester", "proactive checkup", "ifa", "folic"],
    # Nutrition / Anemia
    "anemia": ["anemia", "iron", "आयरन", "ଆଇରନ୍", "hemoglobin", "हीमोग्लोबिन", "ହିମୋଗ୍ଲୋବିନ", "blood deficiency", "खून की कमी", "ରକ୍ତହୀନତା", "spinach", "palak", "ଶାଗ", "leafy", "jaggery", "गुड़", "ଗୁଡ଼"],
    # Diarrhea / ORS
    "diarrhea": ["diarrhea", "ors", "ओआरएस", "ଓଆରଏସ୍", "loose motion", "दस्त", "ତରଳ ଝାଡ଼ା", "dehydration", "निर्जलीकरण", "ଜଳକ୍ଷୟ", "zinc", "जिंक", "ଜିଙ୍କ୍", "rehydration"],
    # Seasonal / Flu
    "flu": ["flu", "influenza", "फ्लू", "ଫ୍ଲୁ", "cough", "खांसी", "କାଶ", "cold", "जुकाम", "ଥଣ୍ଡା", "viral fever", "वायरल बुखार", "ଭୂତାଣୁ ଜ୍ୱର", "paracetamol"]
}


def expand_cross_lingual_tokens(text: str) -> str:
    """Enrich query or passage with bilingual semantic bridges for cross-lingual matching."""
    text_lower = text.lower()
    expansions = []
    for concept, keywords in CROSS_LINGUAL_HEALTH_SYNONYMS.items():
        if any(kw.lower() in text_lower for kw in keywords):
            expansions.append(f"{concept} " + " ".join(keywords))
    if expansions:
        return text + " " + " ".join(expansions)
    return text


class MultilingualEmbedder:
    """
    Multilingual hybrid embedder.
    Combines subword character n-grams (3 to 5) and word n-grams with cross-lingual expansion.
    Optionally calls Gemini API when available.
    """

    def __init__(self, mode: str = "hybrid_tfidf"):
        self.mode = mode
        self.gemini_key = os.getenv("GEMINI_API_KEY")
        self.vectorizer: Optional[TfidfVectorizer] = None
        self._is_fitted = False

    def fit(self, texts: List[str]):
        """Fit the cross-lingual vocabulary on the corpus."""
        enriched_texts = [expand_cross_lingual_tokens(t) for t in texts]
        self.vectorizer = TfidfVectorizer(
            analyzer="char_wb",
            ngram_range=(3, 5),
            min_df=1,
            sublinear_tf=True,
        )
        self.vectorizer.fit(enriched_texts)
        self._is_fitted = True

    def embed_texts(self, texts: List[str]) -> np.ndarray:
        """Generate dense normalized vectors for texts."""
        # Try Gemini API if key is set and mode allows
        if self.gemini_key and self.mode == "gemini":
            try:
                import requests
                embeddings = []
                for text in texts:
                    res = requests.post(
                        f"https://generativelanguage.googleapis.com/v1beta/models/text-embedding-004:embedContent?key={self.gemini_key}",
                        json={"model": "models/text-embedding-004", "content": {"parts": [{"text": text}]}},
                        timeout=5,
                    )
                    if res.status_code == 200:
                        vec = res.json()["embedding"]["values"]
                        embeddings.append(vec)
                    else:
                        break
                if len(embeddings) == len(texts):
                    return normalize(np.array(embeddings, dtype=np.float32))
            except Exception:
                pass  # Fallback to local multilingual vectorizer

        if not self._is_fitted or self.vectorizer is None:
            # Auto-fit if not already fitted
            self.fit(texts)

        enriched = [expand_cross_lingual_tokens(t) for t in texts]
        sparse_vecs = self.vectorizer.transform(enriched)
        dense_vecs = sparse_vecs.toarray().astype(np.float32)
        return normalize(dense_vecs)

    def embed_query(self, query: str) -> np.ndarray:
        """Embed a single query."""
        vec = self.embed_texts([query])
        return vec[0]

    def save(self, filepath: Union[str, Path]):
        """Save fitted vectorizer to disk."""
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "wb") as f:
            pickle.dump(self.vectorizer, f)

    def load(self, filepath: Union[str, Path]):
        """Load fitted vectorizer from disk."""
        with open(filepath, "rb") as f:
            self.vectorizer = pickle.load(f)
            self._is_fitted = True


_GLOBAL_EMBEDDER: Optional[MultilingualEmbedder] = None


def get_embedder() -> MultilingualEmbedder:
    """Singleton getter for the embedder."""
    global _GLOBAL_EMBEDDER
    if _GLOBAL_EMBEDDER is None:
        _GLOBAL_EMBEDDER = MultilingualEmbedder()
    return _GLOBAL_EMBEDDER
