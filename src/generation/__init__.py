"""Generation module for source-grounded answers with citations and language verification."""
from .llm import get_llm_provider, LLMProvider, MockLLMProvider, GeminiProvider
from .generator import GroundedGenerator, GenerationResult
from .citation import extract_citations, Citation
from .language_verifier import verify_language_match, detect_script_language

__all__ = [
    "get_llm_provider",
    "LLMProvider",
    "MockLLMProvider",
    "GeminiProvider",
    "GroundedGenerator",
    "GenerationResult",
    "extract_citations",
    "Citation",
    "verify_language_match",
    "detect_script_language",
]
