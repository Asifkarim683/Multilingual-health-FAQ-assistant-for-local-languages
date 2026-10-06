"""
Query Normalization, Medical Typo Correction, and Query Reception Module.
Handles colloquial phrasings, human typos, phonetic misspellings, transliterated Indic terms,
and short query expansions to ensure robust public health vector retrieval and guardrail compliance.
"""
import re
import difflib
from typing import List, Tuple, Optional, Dict

# Canonical public health vocabulary for fuzzy typo matching
MEDICAL_VOCABULARY = {
    "diarrhea", "diarrhoeal", "dehydration", "rehydration", "ors", "vomiting", "nausea",
    "fever", "dengue", "malaria", "typhoid", "cholera", "tuberculosis", "hypertension",
    "hypotension", "diabetes", "glucose", "insulin", "influenza", "respiratory", "cough",
    "headache", "vaccine", "vaccines", "vaccination", "immunization", "pregnancy",
    "antenatal", "postnatal", "maternal", "pediatric", "infant", "newborn", "anemia",
    "malnutrition", "nutrition", "platelets", "stools", "fluids", "electrolytes", "zinc",
    "mosquito", "infection", "pressure", "symptoms", "prevention", "treatment", "causes",
    "guidelines", "paracetamol", "convulsion", "seizure", "unconscious", "breathing"
}

ENGLISH_STOPWORDS = {
    "what", "when", "where", "which", "with", "from", "that", "this", "have", "does",
    "will", "should", "about", "help", "much", "many", "tell", "show", "give", "some",
    "any", "are", "the", "for", "and", "can", "how", "why", "who", "whom"
}

# Targeted short queries to semantic expansion
SHORT_TOPIC_EXPANSIONS: Dict[str, str] = {
    "diarrhea": "diarrhea causes symptoms dehydration and ORS treatment",
    "diarhea": "diarrhea causes symptoms dehydration and ORS treatment",
    "ors": "ORS oral rehydration salts preparation and zinc therapy for diarrhea",
    "dengue": "dengue fever symptoms prevention warning signs and mosquito control",
    "malaria": "malaria fever symptoms prevention and mosquito vector control",
    "typhoid": "typhoid fever symptoms clean water sanitation and prevention",
    "cholera": "cholera watery diarrhea dehydration and rehydration treatment",
    "tuberculosis": "tuberculosis TB symptoms persistent cough and treatment adherence",
    "tb": "tuberculosis TB symptoms persistent cough and treatment",
    "diabetes": "type 2 diabetes symptoms lifestyle diet blood sugar and screening",
    "hypertension": "hypertension high blood pressure symptoms lifestyle and salt reduction",
    "bp": "high blood pressure hypertension symptoms lifestyle and management",
    "high bp": "high blood pressure hypertension symptoms lifestyle and management",
    "fever": "seasonal fever influenza symptoms red flag signs and home care",
    "vaccine": "recommended vaccine immunization schedule for infants and children",
    "vaccines": "recommended vaccine immunization schedule for infants and children",
    "immunization": "routine immunization schedule for infants and young children",
    "pregnancy": "pregnancy antenatal care maternal health nutrition and danger signs",
    "anemia": "anemia iron deficiency causes symptoms and dietary iron guidance",
}

MEDICAL_TYPO_EXPANSIONS: List[Tuple[str, str]] = [
    # 1. Diarrhea, Dehydration & ORS
    (r"\bdiar+[a-z]*\b", "diarrhea"),
    (r"\bdair+[a-z]*\b", "diarrhea"),
    (r"\bdiarea\b", "diarrhea"),
    (r"\bdiareha\b", "diarrhea"),
    (r"\bdiarrh?oea\b", "diarrhea"),
    (r"\bloose\s+motions?\b", "diarrhea dehydration loose motions"),
    (r"\bwatery\s+stools?\b", "diarrhea dehydration watery stools"),
    (r"\bdast\b", "diarrhea dehydration"),
    (r"\bpet\s+kharab\b", "diarrhea gastrointestinal"),
    (r"\bdehydr+[a-z]*\b", "dehydration"),
    (r"\bdehyra[a-z]*\b", "dehydration"),
    (r"\bdehydartion\b", "dehydration"),
    (r"\bors\b", "ORS oral rehydration salt solution"),
    (r"\bo\.r\.s\b", "ORS oral rehydration salt solution"),
    (r"\bo\s+r\s+s\b", "ORS oral rehydration salt solution"),
    (r"\bvom[i]*t+[a-z]*\b", "vomiting"),
    (r"\bulti\b", "vomiting nausea"),

    # 2. Vector-borne (Dengue, Malaria)
    (r"\bdengu+[a-z]*\b", "dengue"),
    (r"\bdenge\b", "dengue"),
    (r"\bdengue\s+fev[a-z]*\b", "dengue fever"),
    (r"\bmal[ae]r[iy]+a\b", "malaria"),
    (r"\bmaleriya\b", "malaria"),
    (r"\bmachhar\b", "mosquito vector"),
    (r"\bmachharon\b", "mosquito vector"),

    # 3. Water-borne & Bacterial Infections
    (r"\bchol[e]?ra\b", "cholera"),
    (r"\bt[yi]p?ho[iy]d\b", "typhoid"),
    (r"\btipoid\b", "typhoid"),
    (r"\btb\b", "tuberculosis TB"),
    (r"\btubercol[a-z]*\b", "tuberculosis"),
    (r"\btuber[a-z]*\b", "tuberculosis"),

    # 4. Chronic Conditions (Diabetes, Hypertension)
    (r"\bdiabet[a-z]*\b", "diabetes"),
    (r"\bdiabities\b", "diabetes"),
    (r"\bsugar\s+(?:disease|problem|ki\s+bimari|rog)\b", "diabetes blood sugar glucose"),
    (r"\bmadhumeh\b", "diabetes blood sugar"),
    (r"\bhigh\s+bp\b", "hypertension high blood pressure"),
    (r"\bhi\s+bp\b", "hypertension high blood pressure"),
    (r"\blow\s+bp\b", "hypotension low blood pressure"),
    (r"\bbp\b", "blood pressure hypertension"),
    (r"\bhyper\s*tent[a-z]*\b", "hypertension high blood pressure"),
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


def correct_token_spelling(token: str) -> str:
    """Fuzzy match single Latin token against public health dictionary."""
    clean = re.sub(r"[^a-zA-Z]", "", token).lower()
    if len(clean) < 4 or clean in ENGLISH_STOPWORDS or clean in MEDICAL_VOCABULARY:
        return token

    matches = difflib.get_close_matches(clean, MEDICAL_VOCABULARY, n=1, cutoff=0.68)
    return matches[0] if matches else token


def normalize_medical_query_with_details(query: str) -> Tuple[str, Optional[str]]:
    """
    Normalizes typos, colloquial phrases, and single-term queries.
    Returns:
        (effective_query, corrected_query_or_none)
    """
    if not query or not query.strip():
        return "", None

    raw_trimmed = query.strip()
    norm = raw_trimmed

    # 1. Fuzzy token-level typo correction for Latin alphabet queries
    tokens = norm.split()
    corrected_tokens = []
    corrections_made = False

    for tok in tokens:
        corrected = correct_token_spelling(tok)
        if corrected.lower() != tok.lower():
            corrections_made = True
            corrected_tokens.append(corrected)
        else:
            corrected_tokens.append(tok)

    if corrections_made:
        norm = " ".join(corrected_tokens)

    # 2. Targeted regex expansions
    for pattern, repl in MEDICAL_TYPO_EXPANSIONS:
        norm = re.sub(pattern, repl, norm, flags=re.IGNORECASE)

    # 3. Clean consecutive spaces
    norm = re.sub(r"\s+", " ", norm).strip()

    # 4. Check for very short single-topic queries to expand semantics
    lower_norm = norm.lower()
    if lower_norm in SHORT_TOPIC_EXPANSIONS:
        norm = SHORT_TOPIC_EXPANSIONS[lower_norm]

    # Generate friendly human-readable corrected query if meaningful typo fix occurred
    corrected_display = None
    if corrections_made:
        corrected_display = " ".join(corrected_tokens)

    return norm, corrected_display


def normalize_medical_query(query: str) -> str:
    """
    Standard interface returning the effective query string.
    Ensures 100% backward compatibility with all existing callers.
    """
    effective, _ = normalize_medical_query_with_details(query)
    return effective or query
