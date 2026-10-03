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
    "dengue": ["dengue", "डेंगू", "ଡେଙ୍ଗୁ", "ডেঙ্গু", "డెంగ్యూ", "டெங்கு", "aedes", "mosquito", "मच्छर", "ମଶା", "মশা", "దోమ", "கொசு", "platelet"],
    "malaria": ["malaria", "मलेरिया", "ମ୍ୟାଲେରିଆ", "ম্যালেরিয়া", "మలేరియా", "மலேரியா", "mosquito", "fever", "बुखार", "ଜ୍ୱର", "জ্বর", "జ్వరం", "காய்ச்சல்"],
    # Diabetes
    "diabetes": ["diabetes", "डायबिटीज", "ଡାଇବେଟିସ୍", "ডায়াবেটিস", "డయాబెటిస్", "டயாபடீஸ்", "मधुमेह", "ମଧୁମେହ", "বহুমূত্র", "మధుమేహం", "நீரிழிவு", "சர்க்கரை நோய்", "sugar", "शुगर", "ଶୁଗାର", "সুগার", "షుగర్", "சர்க்கரை", "शर्करा", "ଶର୍କରା", "glucose", "insulin", "इंसुलिन"],
    # Hypertension / BP
    "hypertension": ["hypertension", "blood pressure", "ब्लड प्रेशर", "ବ୍ଲଡ ପ୍ରେସର", "ব্লাড প্রেশার", "బ్లడ్ ప్రెజర్", "இரத்த அழுத்தம்", "रक्तचाप", "ରକ୍ତଚାପ", "উচ্চ রক্তচাপ", "రక్తపోటు", "హైపర్‌టెన్షన్", "உயர் இரத்த அழுத்தம்", "ஹைபர்டென்ஷன்", "हाई बीपी", "ହାଇ ବିପି", "salt", "नमक", "ଲୁଣ", "নুন", "ఉప్పు", "உப்பு"],
    # Immunization
    "vaccine": ["vaccine", "immunization", "टीका", "टीकाकरण", "ଟିକା", "ଟୀକାକରଣ", "টিকা", "টিকাদান", "టీకా", "టీకాలు", "தடுப்பூசி", "bcg", "polio", "पोलियो", "ପୋଲିଓ", "পোলিও", "పోలియో", "போலியோ", "pentavalent", "पेंटावेलेंट", "ପେଣ୍ଟାଭାଲେଣ୍ଟ", "পেন্টাভ্যালেন্ট", "పెంటావాలెంట్", "schedule"],
    # Maternal
    "maternal": ["maternal", "pregnancy", "pregnant", "गर्भावस्था", "गर्भवती", "ଗର୍ଭାବସ୍ଥା", "ଗର୍ଭବତୀ", "গর্ভাবস্থা", "গর্ভবতী", "గర్భధారణ", "గర్భిణీ", "கர்ப்பம்", "கர்ப்பிணி", "பிரசவம்", "anc", "pmsma", "trimester", "proactive checkup", "ifa", "folic"],
    # Nutrition / Anemia
    "anemia": ["anemia", "iron", "आयरन", "ଆଇରନ୍", "আয়রন", "ఐరన్", "இரும்புச்சத்து", "hemoglobin", "हीमोग्लोबिन", "ହିମୋଗ୍ଲୋବିନ", "হিমোগ্লোবিন", "హిమోగ్లోబిన్", "ஹீமோகுளோபின்", "blood deficiency", "खून की कमी", "ରକ୍ତହୀନତା", "রক্তস্বল্পতা", "অ্যানিমিয়া", "రక్తహీనత", "అనీమియా", "இரத்த சோகை", "அனீமியா", "spinach", "palak", "ଶାଗ", "শাক", "ఆకుకూరలు", "கீரை", "leafy", "jaggery", "गुड़", "ଗୁଡ଼", "গুড়", "బెల్లం", "வெல்லம்"],
    # Diarrhea / ORS
    "diarrhea": ["diarrhea", "ors", "ओआरएस", "ଓଆରଏସ୍", "ওআরএস", "ఓఆర్ఎస్", "ஓஆர்எஸ்", "loose motion", "दस्त", "ତରଳ ଝାଡ଼ା", "ডায়রিয়া", "পাতলা পায়খানা", "అతిసారం", "విరేచనాలు", "வயிற்றுப்போக்கு", "பேதி", "dehydration", "निर्जलीकरण", "ଜଳକ୍ଷୟ", "পানিশূন্যতা", "నిర్జలీకరణం", "நீரிழப்பு", "zinc", "जिंक", "ଜିଙ୍କ୍", "জিঙ্ক", "జింక్", "ஜிங்க்", "rehydration"],

    # Seasonal / Flu
    "flu": ["flu", "influenza", "फ्लू", "ଫ୍ଲୁ", "ফ্লু", "ఫ్లూ", "cough", "खांसी", "କାଶ", "কাশি", "దగ్గు", "இருமல்", "cold", "जुकाम", "ଥଣ୍ଡା", "সর্দি", "ஜலதோஷம்", "viral fever", "वायरल बुखार", "ଭୂତାଣୁ ଜ୍ୱର", "হিটওয়েভ", "వడదెబ్బ", "வெப்ப அலை", "paracetamol"]
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
