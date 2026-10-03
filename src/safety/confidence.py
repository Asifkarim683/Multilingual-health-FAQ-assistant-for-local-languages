"""Confidence score filtering and out-of-scope refusal logic."""
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
import os


@dataclass
class ConfidenceResult:
    is_sufficient: bool
    top_score: float
    threshold: float
    refusal_message: str


OUT_OF_SCOPE_MESSAGES = {
    "en": "I could not find verified information on this question in my public health database. Please consult a qualified doctor or healthcare professional.",
    "hi": "मुझे अपने सत्यापित स्वास्थ्य स्रोतों में इस विषय पर जानकारी नहीं मिली। कृपया किसी योग्य चिकित्सक या स्वास्थ्य कार्यकर्ता से संपर्क करें।",
    "or": "ମୋର ସତ୍ୟାପିତ ସ୍ୱାସ୍ଥ୍ୟ ତଥ୍ୟରେ ଏହି ପ୍ରଶ୍ନର ଉତ୍ତର ମିଳିଲା ନାହିଁ। ଦୟାକରି ଜଣେ ବିଶେଷଜ୍ଞ ଡାକ୍ତରଙ୍କ ସହ ପରାମର୍ଶ କରନ୍ତୁ।",
}


def check_retrieval_confidence(
    search_results: List[Any],
    language: str = "en",
    threshold: Optional[float] = None,
    config_path: Optional[Any] = None,
) -> ConfidenceResult:
    """
    Check if the top retrieved chunk meets the minimum confidence threshold.
    """
    conf_threshold = threshold
    if conf_threshold is None:
        try:
            conf_threshold = float(os.getenv("CONFIDENCE_THRESHOLD", "0.20"))
        except ValueError:
            conf_threshold = 0.20

    def get_msg():
        if config_path:
            try:
                from src.registry import load_languages_registry
                reg = load_languages_registry(config_path, validate=False)
                if language in reg and "ui_strings" in reg[language]:
                    m = reg[language]["ui_strings"].get("refusal_out_of_scope")
                    if m:
                        return m
            except Exception:
                pass
        return OUT_OF_SCOPE_MESSAGES.get(language, OUT_OF_SCOPE_MESSAGES["en"])

    if not search_results:
        return ConfidenceResult(
            is_sufficient=False,
            top_score=0.0,
            threshold=conf_threshold,
            refusal_message=get_msg(),
        )

    # Get top score
    first_result = search_results[0]
    score = getattr(first_result, "score", None)
    if score is None and isinstance(first_result, dict):
        score = first_result.get("score", 0.0)
    score = float(score or 0.0)

    is_sufficient = score >= conf_threshold
    msg = "" if is_sufficient else get_msg()

    return ConfidenceResult(
        is_sufficient=is_sufficient,
        top_score=score,
        threshold=conf_threshold,
        refusal_message=msg,
    )

