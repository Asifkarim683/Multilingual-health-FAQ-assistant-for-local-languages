"""Emergency keyword detection across English, Hindi, Odia, and registry languages."""
from dataclasses import dataclass
from typing import Optional, Dict, Any, List
import yaml
from pathlib import Path


@dataclass
class EmergencyResult:
    is_emergency: bool
    matched_keyword: Optional[str]
    emergency_message: str


DEFAULT_EMERGENCY_MESSAGES = {
    "en": "EMERGENCY ALERT: Your question indicates a potential medical emergency. Please seek immediate medical attention or call emergency services (112 or 108 in India) without delay.",
    "hi": "आपातकालीन चेतावनी: आपके प्रश्न से गंभीर चिकित्सीय आपात स्थिति का संकेत मिलता है। कृपया तुरंत नजदीकी अस्पताल पहुंचे या आपातकालीन नंबर 112 / 108 पर कॉल करें।",
    "or": "ଜରୁରୀକାଳୀନ ଚେତାବନୀ: ଆପଣଙ୍କ ପ୍ରଶ୍ନରୁ ଗୁରୁତର ସ୍ୱାସ୍ଥ୍ୟ ସଙ୍କଟ ଜଣାପଡୁଛି। ଦୟାକରି ବିଳମ୍ବ ନକରି ତୁରନ୍ତ ଡାକ୍ତରଖାନା ଯାଆନ୍ତୁ କିମ୍ବା ୧୧୨ / ୧୦୮ କୁ ଫୋନ୍ କରନ୍ତୁ।",
}

DEFAULT_KEYWORDS = {
    "en": [
        "chest pain", "heart attack", "difficulty breathing", "cannot breathe",
        "cant breathe", "unconscious", "severe bleeding", "profuse bleeding",
        "poisoning", "swallowed poison", "convulsion", "seizure", "stroke",
        "suicide", "kill myself", "choking"
    ],
    "hi": [
        "सीने में दर्द", "हार्ट अटैक", "सांस लेने में तकलीफ", "सांस फूलना",
        "बेहोश", "बेहोशी", "तेज खून", "खून बहना", "जहर", "दौरा पड़ना",
        "स्ट्रोक", "आत्महत्या", "जान देना"
    ],
    "or": [
        "ଛାତିରେ ଯନ୍ତ୍ରଣା", "ହୃଦଘାତ", "ନିଶ୍ୱାସ ନେବାରେ କଷ୍ଟ", "ଅଚେତ",
        "ପ୍ରଚୁର ରକ୍ତସ୍ରାବ", "ରକ୍ତ ବୋହିବା", "ବିଷ", "ବାତ ମାରିବା", "ଷ୍ଟ୍ରୋକ୍",
        "ଆତ୍ମହତ୍ୟା"
    ],
}


def load_emergency_config(config_path: Path = Path("config/languages.yaml")) -> Dict[str, Dict[str, Any]]:
    """Load emergency keywords and alerts per language from languages.yaml."""
    if not config_path.exists():
        return {}
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            result = {}
            for lang in data.get("languages", []):
                code = lang["code"]
                keywords = lang.get("emergency_keywords", [])
                ui_strings = lang.get("ui_strings", {})
                alert = ui_strings.get("emergency_message", DEFAULT_EMERGENCY_MESSAGES.get(code, DEFAULT_EMERGENCY_MESSAGES["en"]))
                result[code] = {
                    "keywords": keywords,
                    "message": alert,
                }
            return result
    except Exception:
        return {}


def is_keyword_in_query(keyword: str, query: str) -> bool:
    """Check if emergency keyword or key semantic components appear in query."""
    kw_clean = keyword.lower().strip()
    query_clean = query.lower().strip()

    # Exact substring check
    if kw_clean in query_clean:
        return True

    # Multi-token proximity match (e.g. 'सीने में बहुत तेज दर्द' matches 'सीने में दर्द')
    stopwords = {"में", "ରେ", "କିମ୍ବା", "in", "the", "of", "and", "to"}
    key_terms = [w for w in kw_clean.split() if w not in stopwords and len(w) > 1]
    if len(key_terms) >= 2:
        import re
        pattern = r".{0,35}".join(re.escape(w) for w in key_terms)
        if re.search(pattern, query_clean, re.DOTALL):
            return True

    return False


def check_emergency(
    query: str,
    language: str = "en",
    config_path: Path = Path("config/languages.yaml"),
) -> EmergencyResult:
    """
    Check if query contains emergency symptoms.
    Checks language-specific keywords as well as all configured emergency terms.
    """
    query_clean = query.lower().strip()
    registry_config = load_emergency_config(config_path)

    # Keywords for specified language
    lang_info = registry_config.get(language, {})
    keywords = lang_info.get("keywords") or DEFAULT_KEYWORDS.get(language, [])
    alert_msg = lang_info.get("message") or DEFAULT_EMERGENCY_MESSAGES.get(language, DEFAULT_EMERGENCY_MESSAGES["en"])

    # 1. Check primary language keywords
    for kw in keywords:
        if is_keyword_in_query(kw, query_clean):
            return EmergencyResult(
                is_emergency=True,
                matched_keyword=kw,
                emergency_message=alert_msg,
            )

    # 2. Check across all languages (in case user switches script/language within query)
    all_langs = set(list(registry_config.keys()) + list(DEFAULT_KEYWORDS.keys()))
    for other_lang in all_langs:
        other_keywords = registry_config.get(other_lang, {}).get("keywords") or DEFAULT_KEYWORDS.get(other_lang, [])
        for kw in other_keywords:
            if is_keyword_in_query(kw, query_clean):
                return EmergencyResult(
                    is_emergency=True,
                    matched_keyword=kw,
                    emergency_message=alert_msg,
                )

    return EmergencyResult(
        is_emergency=False,
        matched_keyword=None,
        emergency_message="",
    )
