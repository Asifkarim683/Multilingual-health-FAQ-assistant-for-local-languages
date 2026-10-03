"""Prompt template and builder for strictly grounded health question answering."""
from typing import List, Dict, Any

LANGUAGE_NAME_MAP = {
    "en": "English",
    "hi": "Hindi (हिन्दी)",
    "or": "Odia (ଓଡ଼ିଆ)",
    "bn": "Bengali (বাংলা)",
    "te": "Telugu (తెలుగు)",
    "ta": "Tamil (தமிழ்)",
}

SYSTEM_PROMPT = """You are a trustworthy, public health information assistant for Indian communities.
Your mission is to provide accurate, easy-to-understand health information strictly based on verified public health guidelines (WHO, MoHFW India, ICMR, NHM).

CRITICAL GROUNDING RULES:
1. ONLY use information explicitly stated in the provided passages. Do NOT extrapolate or assume.
2. If the answer cannot be found in the passages, you must state: "I could not find this information in my verified public health sources."
3. Strict Medical Safety:
   - NEVER give specific medication dosages (e.g. 'take 500mg').
   - NEVER prescribe prescription medications or brand names.
   - NEVER make a clinical diagnosis (e.g. do not say 'You have dengue').
   - For severe warning signs or emergencies, immediately advise seeing a doctor or emergency services.
4. Target Language:
   - You MUST formulate your answer in {target_language_name}.
   - Use clear, respectful language accessible to rural and urban readers alike.
5. In-text Citations:
   - Cite the source using bracketed numbers like [1], [2] corresponding to the passages provided.
"""


def build_generation_prompt(
    question: str,
    passages: List[Dict[str, Any]],
    target_language: str = "en",
) -> str:
    """Format prompt with numbered source passages and question."""
    lang_name = LANGUAGE_NAME_MAP.get(target_language, "English")

    passages_text = []
    for idx, p in enumerate(passages, 1):
        source_id = p.get("source_id", "SRC")
        title = p.get("title", "Health Source")
        section = p.get("section", "Guidance")
        text = p.get("text", "").strip()
        passages_text.append(f"--- [Passage {idx}] Source: {title} ({source_id}) | Section: {section} ---\n{text}")

    combined_passages = "\n\n".join(passages_text)

    prompt = f"""{SYSTEM_PROMPT.format(target_language_name=lang_name)}

VERIFIED HEALTH PASSAGES:
{combined_passages}

USER QUESTION:
{question}

ANSWER IN {lang_name.upper()} (Strictly grounded in above passages with citations [1], [2]):
"""
    return prompt
