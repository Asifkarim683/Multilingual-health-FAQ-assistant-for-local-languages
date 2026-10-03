"""
BM25 (Best Matching 25) Sparse Keyword Retrieval for Multilingual Health Corpus.
Combines exact lexical matching with Indic script tokenization and Reciprocal Rank Fusion (RRF).
"""
from typing import List, Dict, Set, Optional, Tuple, Union
from pathlib import Path
import math
import pickle
import unicodedata
from collections import Counter, defaultdict
import numpy as np


# Multilingual stopword list across supported languages
STOPWORDS: Set[str] = {
    # English
    "a", "an", "the", "and", "or", "but", "if", "because", "as", "what", "which",
    "who", "whom", "whose", "with", "at", "by", "from", "into", "up", "down",
    "this", "that", "these", "those", "then", "just", "so", "than", "such", "both",
    "through", "about", "for", "is", "of", "while", "during", "to", "in",
    "out", "on", "off", "over", "under", "again", "further", "once", "here", "there",
    "when", "where", "why", "how", "all", "any", "each", "few", "more",
    "most", "other", "some", "no", "nor", "not", "only", "own", "same", "too",
    "very", "can", "will", "should", "now", "are", "was", "were", "be",
    "been", "being", "have", "has", "had", "do", "does", "did", "doing", "today",
    # Hindi (हिन्दी)
    "है", "हैं", "के", "की", "का", "को", "में", "से", "पर", "और", "या", "तो",
    "भी", "यह", "वह", "क्या", "हुआ", "हुए", "हुई", "द्वारा", "था", "थे", "थी",
    "कौन", "किस", "किसे", "किसका", "कैसे", "कहाँ", "कब",
    # Odia (ଓଡ଼ିଆ)
    "ହେଉଛି", "ଏବଂ", "ଓ", "ବା", "ର", "କୁ", "ରେ", "କଣ", "କିପରି", "ଏହି", "ସେହି",
    "ଦ୍ୱାରା", "ପାଇଁ", "ଥିଲା", "ଅଟେ", "କିଏ", "କାହାକୁ", "କେଉଁଠାରେ",
    # Bengali (বাংলা)
    "হয়", "এবং", "ও", "বা", "এর", "কে", "তে", "কি", "কিভাবে", "এই", "সেই",
    "দ্বারা", "জন্য", "ছিল", "কে", "কার", "কোথায়", "কখন",
    # Telugu (తెలుగు)
    "మరియు", "లేదా", "యొక్క", "లో", "కి", "కు", "ఏమిటి", "ఎలా", "ఈ", "ఆ",
    "ద్వారా", "కోసం", "ఎవరు", "ఎక్కడ", "ఎప్పుడు",
    # Tamil (தமிழ்)
    "மற்றும்", "அல்லது", "இன்", "இல்", "க்கு", "என்ன", "எப்படி", "இந்த", "அந்த",
    "மூலம்", "ஆகும்", "யார்", "எங்கு", "எப்போது",
}


def tokenize_multilingual(text: str, filter_stopwords: bool = True) -> List[str]:
    """
    Tokenize multilingual text including Latin and Indic scripts (Devanagari, Odia, Bengali, Telugu, Tamil).
    Preserves full Unicode word tokens (Letters, Combining Marks/Matras, Numbers)
    while filtering punctuation, symbols, and language stopwords.
    """
    if not text:
        return []

    text = text.lower()
    tokens: List[str] = []
    current: List[str] = []

    for char in text:
        # Letters ('L'), Combining Marks/Matras ('M'), and Numbers ('N')
        cat = unicodedata.category(char)
        if cat.startswith(("L", "M", "N")):
            current.append(char)
        else:
            if current:
                token = "".join(current)
                if (not filter_stopwords or token not in STOPWORDS) and len(token) > 1:
                    tokens.append(token)
                current = []

    if current:
        token = "".join(current)
        if (not filter_stopwords or token not in STOPWORDS) and len(token) > 1:
            tokens.append(token)

    return tokens


class BM25Index:
    """
    BM25 Okapi retrieval implementation supporting multilingual and cross-script queries.
    Parameters:
        k1: Term frequency saturation parameter (default: 1.5).
        b: Document length normalization parameter (default: 0.75).
    """

    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.corpus_size: int = 0
        self.avg_doc_len: float = 0.0
        self.doc_lens: List[int] = []
        self.doc_term_freqs: List[Counter] = []
        self.doc_freqs: Dict[str, int] = defaultdict(int)
        self.idf: Dict[str, float] = {}

    def fit(self, corpus: List[str]):
        """Build term frequencies, document frequencies, and IDF values across corpus."""
        self.corpus_size = len(corpus)
        if self.corpus_size == 0:
            return

        self.doc_lens = []
        self.doc_term_freqs = []
        self.doc_freqs = defaultdict(int)

        total_len = 0
        for doc in corpus:
            tokens = tokenize_multilingual(doc)
            doc_len = len(tokens)
            self.doc_lens.append(doc_len)
            total_len += doc_len

            tf = Counter(tokens)
            self.doc_term_freqs.append(tf)

            for term in tf:
                self.doc_freqs[term] += 1

        self.avg_doc_len = total_len / self.corpus_size if self.corpus_size > 0 else 0.0

        # Calculate BM25 IDF for each term:
        # IDF(t) = ln( 1 + (N - DF + 0.5) / (DF + 0.5) )
        self.idf = {}
        for term, df in self.doc_freqs.items():
            self.idf[term] = math.log(1.0 + (self.corpus_size - df + 0.5) / (df + 0.5))

    def get_scores(self, query: str) -> np.ndarray:
        """Calculate BM25 scores for query across all indexed documents."""
        scores = np.zeros(self.corpus_size, dtype=np.float32)
        if self.corpus_size == 0:
            return scores

        query_tokens = tokenize_multilingual(query)
        if not query_tokens:
            return scores

        for token in query_tokens:
            if token not in self.idf:
                continue

            idf = self.idf[token]
            for doc_idx, tf_counter in enumerate(self.doc_term_freqs):
                tf = tf_counter.get(token, 0)
                if tf == 0:
                    continue

                doc_len = self.doc_lens[doc_idx]
                denom = tf + self.k1 * (1.0 - self.b + self.b * (doc_len / self.avg_doc_len if self.avg_doc_len > 0 else 1.0))
                score_t = idf * (tf * (self.k1 + 1.0)) / denom
                scores[doc_idx] += score_t

        return scores

    def save(self, file_path: Union[str, Path]):
        """Serialize BM25 index state to disk."""
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        state = {
            "k1": self.k1,
            "b": self.b,
            "corpus_size": self.corpus_size,
            "avg_doc_len": self.avg_doc_len,
            "doc_lens": self.doc_lens,
            "doc_term_freqs": self.doc_term_freqs,
            "doc_freqs": dict(self.doc_freqs),
            "idf": self.idf,
        }
        with open(path, "wb") as f:
            pickle.dump(state, f)

    @classmethod
    def load(cls, file_path: Union[str, Path]) -> "BM25Index":
        """Load BM25 index state from disk."""
        path = Path(file_path)
        with open(path, "rb") as f:
            state = pickle.load(f)
        index = cls(k1=state["k1"], b=state["b"])
        index.corpus_size = state["corpus_size"]
        index.avg_doc_len = state["avg_doc_len"]
        index.doc_lens = state["doc_lens"]
        index.doc_term_freqs = state["doc_term_freqs"]
        index.doc_freqs = defaultdict(int, state["doc_freqs"])
        index.idf = state["idf"]
        return index


def reciprocal_rank_fusion(
    dense_ranks: List[int],
    sparse_ranks: List[int],
    sparse_scores: Optional[np.ndarray] = None,
    k: int = 60,
    w_dense: float = 0.6,
    w_sparse: float = 0.4,
) -> Dict[int, float]:
    """
    Combine rankings using Reciprocal Rank Fusion (RRF).
    RRF(d) = w_dense / (k + rank_dense) + w_sparse / (k + rank_sparse)
    Only documents with non-zero sparse score receive sparse rank points.
    """
    rrf_scores: Dict[int, float] = defaultdict(float)

    for rank, doc_idx in enumerate(dense_ranks, 1):
        rrf_scores[doc_idx] += w_dense / (k + rank)

    for rank, doc_idx in enumerate(sparse_ranks, 1):
        # Only assign sparse points if the document actually matched query tokens
        if sparse_scores is None or sparse_scores[doc_idx] > 0:
            rrf_scores[doc_idx] += w_sparse / (k + rank)

    return rrf_scores
