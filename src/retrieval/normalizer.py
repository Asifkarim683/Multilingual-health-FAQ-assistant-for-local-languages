"""
Query Normalization and Medical Typo Correction Module.
Handles colloquial phrasings, typos, phonetic misspellings, and keyword expansions
to ensure robust public health vector retrieval and guardrail compliance.
"""
import re
from typing import List, Tuple

MEDICAL_TYPO_EXPANSIONS: List[Tuple[str, str]] = [
    # 1. Diarrhea, Dehydration & ORS
    (r"\bdiar+h?e+a?\b", "diarrhea"),
    (r"\bdiarrh?oea\b", "diarrhea"),
    (r"\bdiarea\b", "diarrhea"),
    (r"\bdiareha\b", "diarrhea"),
    (r"\bloose\s+motions?\b", "diarrhea dehydration"),
    (r"\bwatery\s+stools?\b", "diarrhea dehydration watery stools"),
    (r"\bdast\b", "diarrhea dehydration"),
    (r"\bpet\s+kharab\b", "diarrhea gastrointestinal"),
    (r"\bdehyra[a-z]*\b", "dehydration"),
    (r"\bdehydrat[a-z]*\b", "dehydration"),
    (r"\bdehydartion\b", "dehydration"),
    (r"\bors\b", "ORS oral rehydration salt solution"),
    (r"\bo\.r\.s\b", "ORS oral rehydration salt solution"),
    (r"\bo\s+r\s+s\b", "ORS oral rehydration salt solution"),
    (r"\bvomi[t]*ing\b", "vomiting"),
    (r"\bvomting\b", "vomiting"),
    (r"\bulti\b", "vomiting nausea"),

    # 2. Vector-borne (Dengue, Malaria)
    (r"\bdengu[e]?\b", "dengue"),
    (r"\bdenge\b", "dengue"),
    (r"\bdengue\s+fev[a-z]*\b", "dengue fever"),
    (r"\bmal[ae]r[iy]+a\b", "malaria"),
    (r"\bmaleriya\b", "malaria"),
    (r"\bmachhar\b", "mosquito vector"),
    (r"\bmachharon\b", "mosquito vector"),

    # 3. Water-borne & Bacterial Infections
    (r"\bc[ho]+lera\b", "cholera"),
    (r"\bcholra\b", "cholera"),
    (r"\bt[yi]p?ho[iy]d\b", "typhoid"),
    (r"\btipoid\b", "typhoid"),
    (r"\btb\b", "tuberculosis TB"),
    (r"\btuber[a-z]*\b", "tuberculosis"),
    (r"\btubercolosis\b", "tuberculosis"),

    # 4. Chronic Conditions (Diabetes, Hypertension)
    (r"\bdiabet[a-z]*\b", "diabetes"),
    (r"\bdiabities\b", "diabetes"),
    (r"\bdiabete\b", "diabetes"),
    (r"\bsugar\s+(?:disease|problem|ki\s+bimari|rog)\b", "diabetes blood sugar glucose"),
    (r"\bmadhumeh\b", "diabetes blood sugar"),
    (r"\bhigh\s+bp\b", "hypertension high blood pressure"),
    (r"\bhi\s+bp\b", "hypertension high blood pressure"),
    (r"\blow\s+bp\b", "hypotension low blood pressure"),
    (r"\bbp\b", "blood pressure hypertension"),
    (r"\bhyper\s*tension\b", "hypertension high blood pressure"),
    (r"\braktachap\b", "hypertension blood pressure"),

    # 5. Fevers & Respiratory Infections
    (r"\bfev[a-z]*\b", "fever"),
    (r"\bbukhar\b", "fever"),
    (r"\bjwar[a]?\b", "fever"),
    (r"\bflu\b", "influenza viral fever"),
    (r"\binflu[a-z]*\b", "influenza viral fever"),
    (r"\bcold\s+(?:and|&)\s+cough\b", "respiratory infection viral fever cold cough"),
    (r"\bkhansi\b", "cough respiratory"),
    (r"\bsardi\b", "cold flu fever"),
    (r"\bhead\s*ach[e]?\b", "headache"),
    (r"\bsir\s+dard\b", "headache"),

    # 6. Maternal, Child & Immunization
    (r"\bpregnan[a-z]*\b", "pregnancy antenatal care"),
    (r"\bantenat[a-z]*\b", "antenatal care pregnancy"),
    (r"\bgarbhavastha\b", "pregnancy maternal"),
    (r"\bva[ck]+in[a-z]*\b", "vaccine immunization schedule"),
    (r"\bvacination\b", "vaccine immunization"),
    (r"\bteeka\b", "vaccine immunization"),
    (r"\btika\b", "vaccine immunization"),
    (r"\btikakaran\b", "vaccine immunization schedule"),
    (r"\bshishu\b", "infant child immunization"),
    (r"\bnew\s*born\b", "newborn infant baby"),
    (r"\banem[iy]+a\b", "anemia iron deficiency hemoglobin"),
    (r"\bkhoon\s+ki\s+kami\b", "anemia iron deficiency"),
    (r"\bmal\s*nutrit[a-z]*\b", "malnutrition balanced nutrition"),
]


def normalize_medical_query(query: str) -> str:
    """
    Normalizes common medical typos, expands colloquial acronyms (like ORS, BP, TB),
    and aligns user queries with the public health clinical knowledge corpus.
    """
    if not query:
        return ""

    cleaned = query.strip()
    norm = cleaned

    for pattern, repl in MEDICAL_TYPO_EXPANSIONS:
        norm = re.sub(pattern, repl, norm, flags=re.IGNORECASE)

    # Clean multi-spaces
    norm = re.sub(r"\s+", " ", norm).strip()
    return norm
