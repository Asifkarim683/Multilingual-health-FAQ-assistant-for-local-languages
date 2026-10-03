"""Detection and refusal for medication dosage, prescription, and clinical diagnosis requests."""
from dataclasses import dataclass
from typing import Optional, List, Any
import re



@dataclass
class DosageRefusalResult:
    is_refusal: bool
    reason: Optional[str]  # 'dosage' | 'diagnosis'
    refusal_message: str


DOSAGE_REFUSAL_MESSAGES = {
    "en": "I cannot provide medication dosage, prescription, or clinical diagnosis. Only a qualified medical doctor can prescribe drugs or diagnose health conditions. Please visit a registered healthcare professional.",
    "hi": "मैं दवा की खुराक, नुस्खा या बीमारी का निदान नहीं बता सकता। केवल योग्य डॉक्टर ही दवाएं लिख सकते हैं या रोग का निदान कर सकते हैं। कृपया किसी पंजीकृत चिकित्सक से सलाह लें।",
    "or": "ମୁଁ ଔଷଧର ମାତ୍ରା ବା ରୋଗ ନିର୍ଣ୍ଣୟ ସମ୍ପର୍କରେ ପରାମର୍ଶ ଦେଇପାରିବି ନାହିଁ। କେବଳ ପଞ୍ଜୀକୃତ ଡାକ୍ତର ହିଁ ଔଷଧ ଲେଖିପାରିବେ ବା ରୋଗ ନିର୍ଣ୍ଣୟ କରିପାରିବେ। ଦୟାକରି ଡାକ୍ତରଙ୍କୁ ଦେଖାନ୍ତୁ।",
}

DOSAGE_PATTERNS = [
    # English
    r"\b(how much|how many)\s+(mg|milligram|tablets?|pills?|doses?|drops?)\b",
    r"\b(what\s+dose|dosage\s+of|prescription\s+for|which\s+(tablet|pill|medicine|drug)\s+(should|can)\s+i\s+take)\b",
    r"\b(take\s+\d+\s*mg|prescribe\s+me)\b",
    # Hindi
    r"(कितनी?|कितने|कितना)\s*(खुराक|गोली|गोलियां|एमजी|मिलीग्राम|दवा|टैबलेट)",
    r"(कौन\s*सी\s*(दवा|गोली|टैबलेट)\s*(लूं|खाऊं|पीऊं))",
    r"(दवा\s*का\s*नाम\s*बताएं|नुस्खा|प्रिस्क्रिप्शन)",
    # Odia
    r"(କେତେ(ଟା|ଟି|ୋଟି)?\s*(ମିଗ୍ରା|ମିଲିଗ୍ରାମ|ବଟିକା|ଔଷଧ|ମାତ୍ରା|ଡୋଜ୍|ଟାବଲେଟ))",
    r"(କେଉଁ\s*(ଔଷଧ|ବଟିକା|ଟାବଲେଟ୍?)\s*(ଖାଇବି|ନେବି))",
    r"(ଔଷଧର\s*ନାମ\s*(କୁହନ୍ତୁ|ଦିଅନ୍ତୁ))",
]

DIAGNOSIS_PATTERNS = [
    # English
    r"\b(do\s+i\s+have|diagnose\s+me|tell\s+me\s+my\s+disease|what\s+illness\s+do\s+i\s+have)\b",
    r"\b(am\s+i\s+suffering\s+from|do\s+these\s+symptoms\s+mean\s+i\s+have)\b",
    # Hindi
    r"(क्या\s*मुझे\s*(कैंसर|टीबी|बीमारी|रोग)\s*है)",
    r"(मुझे\s*कौन\s*सी\s*बीमारी\s*है|मेरा\s*रोग\s*बताएं)",
    # Odia
    r"(ମୋର\s*କେଉଁ\s*ରୋଗ\s*ହୋଇଛି|ମୋତେ\s*କ୍ୟାନସର\s*ହୋଇଛି\s*କି)",
    r"(ରୋଗ\s*ନିର୍ଣ୍ଣୟ\s*କରନ୍ତୁ)",
]


def check_dosage_or_diagnosis(
    query: str,
    language: str = "en",
    config_path: Optional[Any] = None,
) -> DosageRefusalResult:
    """Check if query requests medication dosing, prescription, or clinical diagnosis."""
    query_lower = query.lower()

    def get_msg():
        if config_path:
            try:
                from src.registry import load_languages_registry
                reg = load_languages_registry(config_path, validate=False)
                if language in reg and "ui_strings" in reg[language]:
                    m = reg[language]["ui_strings"].get("refusal_dosage")
                    if m:
                        return m
            except Exception:
                pass
        return DOSAGE_REFUSAL_MESSAGES.get(language, DOSAGE_REFUSAL_MESSAGES["en"])

    # Check dosage patterns
    for pat in DOSAGE_PATTERNS:
        if re.search(pat, query_lower):
            return DosageRefusalResult(
                is_refusal=True,
                reason="dosage",
                refusal_message=get_msg(),
            )

    # Check diagnosis patterns
    for pat in DIAGNOSIS_PATTERNS:
        if re.search(pat, query_lower):
            return DosageRefusalResult(
                is_refusal=True,
                reason="diagnosis",
                refusal_message=get_msg(),
            )


    return DosageRefusalResult(
        is_refusal=False,
        reason=None,
        refusal_message="",
    )
