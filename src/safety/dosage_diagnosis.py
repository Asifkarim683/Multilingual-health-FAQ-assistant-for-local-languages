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
    r"(खुराक\s*कितनी?|(कितनी?|कितने|कितना)\s*(खुराक|गोली|गोलियां|एमजी|मिलीग्राम|दवा|टैबलेट))",
    r"(खुराक|डोज|डोज़)\s*(कितनी?|क्या|बताएं|होनी)",
    r"(कौन\s*सी\s*(दवा|गोली|टैबलेट)\s*(लूं|खाऊं|पीऊं))",
    r"(दवा\s*का\s*नाम\s*बताएं|नुस्खा|प्रिस्क्रिप्शन|की\s*खुराक)",
    # Odia
    r"(କେତେ(ଟା|ଟି|ୋଟି)?\s*(ମିଗ୍ରା|ମିଲିଗ୍ରାମ|ବଟିକା|ଔଷଧ|ମାତ୍ରା|ଡୋଜ୍|ଟାବଲେଟ))",
    r"(ଔଷଧର\s*ମାତ୍ରା|ଡୋଜ୍\s*କେତେ)",
    r"(କେଉଁ\s*(ଔଷଧ|ବଟିକା|ଟାବଲେଟ୍?)\s*(ଖାଇବି|ନେବି))",
    r"(ଔଷଧର\s*ନାମ\s*(କୁହନ୍ତୁ|ଦିଅନ୍ତୁ))",
    # Bengali
    r"(কত(টা|টুকু)?|কয়টি)\s*(ট্যাবলেট|ওষুধ|ডোজ|মিলিগ্রাম|এমজি|মাত্রা)",
    r"(ডোজ|মাত্রা|ওষুধের\s*পরিমাণ)\s*(কত|কী|বলুন)",
    r"(কোন\s*ওষুধ\s*(খাব|নেব|খাওয়া\s*উচিত)|ওষুধের\s*নাম\s*(বলুন|দিন))",
    # Telugu
    r"(ఎంత|ఎన్ని)\s*(మాత్రలు|టాబ్లెట్|మోతాదు|మిల్లీగ్రామ్|మిల్లీగ్రాముల|ఎంజీ|మందు)",
    r"(మోతాదు|డోస్)\s*(ఎంత|ఏమిటి|చెప్పండి)",
    r"(ఏ\s*మందు\s*(వేసుకోవాలి|వాడాలి|తాగాలి)|మందు\s*పేరు\s*(చెప్పండి|ఇవ్వండి))",
    # Tamil
    r"(எவ்வளவு|எத்தனை)\s*(மாத்திரை|மருந்து|அளவு|மருந்தளவு|டோஸ்|மில்லிகிராம்|எம்ஜி)",
    r"(மருந்தளவு|அளவு|டோஸ்)\s*(என்ன|எவ்வளவு|சொல்லுங்கள்)",
    r"(என்ன\s*மருந்து\s*(சாப்பிட|எடுக்க|போட\s*வேண்டும்)|மருந்தின்\s*பெயர்\s*(சொல்லுங்கள்|கொடுங்கள்))",
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
    # Bengali
    r"(আমার\s*কী\s*রোগ\s*হয়েছে|আমাকে\s*কি\s*(ক্যান্সার|টিবি|রোগ)\s*হয়েছে)",
    r"(রোগ\s*নির্ণয়\s*করুন)",
    # Telugu
    r"(నాకు\s*ఏ\s*వ్యాధి\s*ఉంది|నాకు\s*(క్యాన్సర్|టీబీ|రోfloat|వ్యాధి)\s*వచ్చిందా)",
    r"(రోగ\s*నిర్ధారణ\s*చేయండి)",
    # Tamil
    r"(எனக்கு\s*என்ன\s*நோய்\s*உள்ளது|எனக்கு\s*(புற்றுநோய்|நோய்)\s*உள்ளதா)",
    r"(நோயறிதல்\s*செய்யவும்)",
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
