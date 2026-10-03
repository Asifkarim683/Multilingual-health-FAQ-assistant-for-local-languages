"""Grounded generator orchestrating prompt construction, LLM generation, citation extraction, and post-checks."""
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional
import uuid
import yaml
from pathlib import Path

from .llm import get_llm_provider, LLMProvider
from .prompt import build_generation_prompt
from .citation import extract_citations, Citation
from .language_verifier import verify_language_match, detect_script_language


@dataclass
class GenerationResult:
    answer: str
    language: str
    status: str
    citations: List[Dict[str, Any]]
    disclaimer: str
    request_id: str
    language_match: bool
    source_passages: List[Dict[str, Any]]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "answer": self.answer,
            "language": self.language,
            "status": self.status,
            "citations": self.citations,
            "disclaimer": self.disclaimer,
            "request_id": self.request_id,
            "language_match": self.language_match,
            "source_passages": self.source_passages,
        }


class GroundedGenerator:
    """Manages generation of grounded health responses from retrieved passages."""

    def __init__(
        self,
        llm_provider: Optional[LLMProvider] = None,
        config_path: Path = Path("config/languages.yaml"),
    ):
        self.llm = llm_provider or get_llm_provider()
        self.languages_config = self._load_languages(config_path)

    def _load_languages(self, config_path: Path) -> Dict[str, Any]:
        if config_path.exists():
            with open(config_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                return {lang["code"]: lang for lang in data.get("languages", [])}
        return {}

    def get_disclaimer(self, lang_code: str) -> str:
        lang_info = self.languages_config.get(lang_code)
        if lang_info and lang_info.get("disclaimer"):
            return lang_info["disclaimer"]
        # Default fallback disclaimer
        return (
            "This assistant provides verified public health information for general awareness only. "
            "It does not provide medical diagnosis, treatment, or dosage advice. Always consult a qualified "
            "healthcare provider for medical concerns. In an emergency, call 112 / 108 immediately."
        )

    def generate_response(
        self,
        question: str,
        retrieved_chunks: List[Dict[str, Any]],
        target_language: str = "auto",
        request_id: Optional[str] = None,
    ) -> GenerationResult:
        """
        Generate answer strictly grounded in retrieved chunks.
        Performs language verification and citation extraction.
        """
        req_id = request_id or str(uuid.uuid4())

        # 1. Resolve Language
        if target_language == "auto" or not target_language:
            resolved_lang = detect_script_language(question)
        else:
            resolved_lang = target_language

        disclaimer = self.get_disclaimer(resolved_lang)

        # 2. Check if chunks are provided
        if not retrieved_chunks:
            refusal_text = (
                "I could not find verified information on this topic in my public health database. "
                "Please consult a doctor or healthcare worker for personal medical guidance."
            )
            if resolved_lang == "hi":
                refusal_text = "मुझे अपने सत्यापित स्वास्थ्य स्रोतों में इस विषय पर जानकारी नहीं मिली। कृपया किसी योग्य चिकित्सक से संपर्क करें।"
            elif resolved_lang == "or":
                refusal_text = "ମୋର ସତ୍ୟାପିତ ସ୍ୱାସ୍ଥ୍ୟ ତଥ୍ୟରେ ଏହି ପ୍ରଶ୍ନର ଉତ୍ତର ମିଳିଲା ନାହିଁ। ଦୟାକରି ଜଣେ ବିଶେଷଜ୍ଞ ଡାକ୍ତରଙ୍କ ସହ ପରାମର୍ଶ କରନ୍ତୁ।"

            return GenerationResult(
                answer=refusal_text,
                language=resolved_lang,
                status="refused",
                citations=[],
                disclaimer=disclaimer,
                request_id=req_id,
                language_match=True,
                source_passages=[],
            )

        # 3. Build Prompt & Generate
        prompt = build_generation_prompt(
            question=question,
            passages=retrieved_chunks,
            target_language=resolved_lang,
        )
        raw_answer = self.llm.generate(prompt=prompt, target_lang=resolved_lang)

        # 4. Post-Checks: Language Match
        is_lang_match, detected = verify_language_match(raw_answer, resolved_lang)

        # 5. Extract Citations
        citations = extract_citations(raw_answer, retrieved_chunks)

        return GenerationResult(
            answer=raw_answer,
            language=resolved_lang,
            status="answered",
            citations=[c.to_dict() for c in citations],
            disclaimer=disclaimer,
            request_id=req_id,
            language_match=is_lang_match,
            source_passages=[
                {
                    "source_id": c.get("source_id"),
                    "title": c.get("title"),
                    "text": c.get("text"),
                    "url": c.get("url"),
                }
                for c in retrieved_chunks[:3]
            ],
        )
