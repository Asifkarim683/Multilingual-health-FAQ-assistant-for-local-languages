"""FastAPI Application for Multilingual Health FAQ Assistant."""
from fastapi import FastAPI, HTTPException, Request, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pathlib import Path
import uuid
import yaml
import os
from typing import Dict, Any, List

from .schemas import (
    AskRequest,
    AskResponse,
    CitationItem,
    FeedbackRequest,
    FeedbackResponse,
    HealthResponse,
    LanguageInfo,
)
from .database import init_db, log_query, save_feedback
from .rate_limiter import rate_limiter
from src.retrieval.vector_store import VectorStore
from src.safety.guardrails import SafetyGuardrail
from src.generation.generator import GroundedGenerator
from src.generation.language_verifier import detect_script_language

# Global State / Singletons
_VECTOR_STORE: VectorStore = None
_GUARDRAIL: SafetyGuardrail = None
_GENERATOR: GroundedGenerator = None
_LANGUAGES_REGISTRY: Dict[str, Any] = {}


def get_services():
    global _VECTOR_STORE, _GUARDRAIL, _GENERATOR, _LANGUAGES_REGISTRY
    if _VECTOR_STORE is None:
        chunks_path = Path("data/processed/chunks.json")
        if not chunks_path.exists():
            from src.ingestion.run import run_ingestion
            run_ingestion()
        _VECTOR_STORE = VectorStore.from_processed_chunks(chunks_path)

    if _GUARDRAIL is None:
        _GUARDRAIL = SafetyGuardrail()

    if _GENERATOR is None:
        _GENERATOR = GroundedGenerator()

    if not _LANGUAGES_REGISTRY:
        config_path = Path("config/languages.yaml")
        if config_path.exists():
            from src.registry import load_languages_registry
            _LANGUAGES_REGISTRY = load_languages_registry(config_path, validate=True)

    return _VECTOR_STORE, _GUARDRAIL, _GENERATOR, _LANGUAGES_REGISTRY



from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    get_services()
    yield

app = FastAPI(
    title="Multilingual Health FAQ Assistant API",
    description="Grounded health question answering in Indian languages (Hindi, Odia, Bengali, Telugu, Tamil, English) with verifiable citations and strict safety guardrails.",
    version="1.1.0",
    lifespan=lifespan,
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health", response_model=HealthResponse)
def health_check():
    """Health check endpoint providing system status and knowledge base statistics."""
    store, _, _, registry = get_services()
    return HealthResponse(
        status="healthy",
        version="1.1.0",
        knowledge_base_version="1.1",
        total_chunks=len(store.chunks),
        supported_languages=list(registry.keys()),
    )


@app.get("/api/languages", response_model=List[LanguageInfo])
def get_languages():
    """Retrieve full language registry including native names, fonts, statuses, and UI strings."""
    _, _, _, registry = get_services()
    results = []
    for code, info in registry.items():
        results.append(
            LanguageInfo(
                code=code,
                name=info.get("name", code),
                native_name=info.get("native_name", code),
                script=info.get("script", "Unknown"),
                font=info.get("font", "sans-serif"),
                status=info.get("status", "experimental"),
                example_questions=info.get("example_questions", []),
                ui_strings=info.get("ui_strings", {}),
            )
        )
    return results


_ask_cache: dict[str, AskResponse] = {}
_tts_audio_cache: dict[str, bytes] = {}


@app.post("/api/ask", response_model=AskResponse)
def ask_question(req: AskRequest, request: Request):
    """
    Main endpoint answering health queries with medical guardrails, citations, and disclaimer.
    """
    client_ip = request.client.host if request.client else "unknown"
    rate_limiter.check(client_ip)

    store, guardrail, generator, registry = get_services()
    req_id = str(uuid.uuid4())

    # 1. Resolve Language
    if not req.language or req.language == "auto":
        resolved_lang = detect_script_language(req.question)
    else:
        resolved_lang = req.language

    # Check In-Memory Query & Translation Cache for instant response (< 5ms)
    norm_q = req.question.strip().lower()
    cache_key = f"{norm_q}____{resolved_lang}"
    if cache_key in _ask_cache:
        cached_resp = _ask_cache[cache_key]
        log_query(req_id, resolved_lang, cached_resp.status, len(req.question), len(cached_resp.citations))
        return AskResponse(
            answer=cached_resp.answer,
            language=cached_resp.language,
            status=cached_resp.status,
            citations=cached_resp.citations,
            disclaimer=cached_resp.disclaimer,
            request_id=req_id,
            is_experimental=cached_resp.is_experimental,
        )

    lang_meta = registry.get(resolved_lang, {})
    is_experimental = lang_meta.get("status", "stable") == "experimental"
    disclaimer = generator.get_disclaimer(resolved_lang)

    # 2. Safety Pre-Check (Emergency & Dosage / Clinical Diagnosis)
    pre_check = guardrail.run_pre_check(req.question, language=resolved_lang)
    if pre_check.action == "emergency":
        log_query(req_id, resolved_lang, "emergency", len(req.question), 0)
        return AskResponse(
            answer=pre_check.message,
            language=resolved_lang,
            status="emergency",
            citations=[],
            disclaimer=disclaimer,
            request_id=req_id,
            is_experimental=is_experimental,
        )

    if pre_check.action == "refused":
        log_query(req_id, resolved_lang, "refused", len(req.question), 0)
        return AskResponse(
            answer=pre_check.message,
            language=resolved_lang,
            status="refused",
            citations=[],
            disclaimer=disclaimer,
            request_id=req_id,
            is_experimental=is_experimental,
        )

    # 3. Vector Retrieval
    results = store.search(req.question, top_k=5, lang_filter=resolved_lang)


    # 4. Safety Post-Check (Confidence Filtering for Out-of-Scope)
    post_check = guardrail.run_post_retrieval_check(results, language=resolved_lang, threshold=0.20)
    if post_check.action == "refused":
        log_query(req_id, resolved_lang, "refused", len(req.question), 0)
        return AskResponse(
            answer=post_check.message,
            language=resolved_lang,
            status="refused",
            citations=[],
            disclaimer=disclaimer,
            request_id=req_id,
            is_experimental=is_experimental,
        )

    # 5. Grounded Generation
    top_chunks = [r.to_dict() for r in results]
    gen_result = generator.generate_response(
        question=req.question,
        retrieved_chunks=top_chunks,
        target_language=resolved_lang,
        request_id=req_id,
    )

    log_query(
        req_id,
        resolved_lang,
        gen_result.status,
        len(req.question),
        len(gen_result.citations),
    )

    citation_items = [CitationItem(**c) for c in gen_result.citations]

    response = AskResponse(
        answer=gen_result.answer,
        language=gen_result.language,
        status=gen_result.status,  # type: ignore
        citations=citation_items,
        disclaimer=gen_result.disclaimer,
        request_id=gen_result.request_id,
        is_experimental=is_experimental,
    )

    # Store in memory cache for subsequent instant queries / language switches
    if len(_ask_cache) > 500:
        _ask_cache.pop(next(iter(_ask_cache)))
    _ask_cache[cache_key] = response

    return response


@app.post("/api/feedback", response_model=FeedbackResponse)
def submit_feedback(req: FeedbackRequest):
    """Store thumbs up / down rating and comment."""
    save_feedback(req.request_id, req.rating, req.comment)
    return FeedbackResponse(
        status="success",
        message="Feedback successfully recorded.",
    )


def odia_to_phonetic_devanagari(text: str) -> str:
    """
    Phonetically maps Odia Unicode script (U+0B00-U+0B7F) to Devanagari (U+0900-U+097F)
    so Google Indic TTS voices synthesize natural, fluent Odia speech.
    """
    custom_map = {
        0x0B5F: '\u092F',  # ୟ (Odia ya) -> य
        0x0B71: '\u0935',  # ୱ (Odia wa) -> व
        0x0B33: '\u0933',  # ଳ (Odia lla) -> ळ
        0x0B5C: '\u095C',  # ଡ଼ (Odia rra) -> ड़
        0x0B5D: '\u095D',  # ଢ଼ (Odia rha) -> ढ़
        0x0B02: '\u0902',  # ଂ (Anusvara) -> ं
        0x0B03: '\u0903',  # ଃ (Visarga) -> ः
        0x0B01: '\u0901',  # ଁ (Candrabindu) -> ँ
    }
    out = []
    for ch in text:
        cp = ord(ch)
        if cp in custom_map:
            out.append(custom_map[cp])
        elif 0x0B05 <= cp <= 0x0B70:
            out.append(chr(cp - 0x0200))
        else:
            out.append(ch)
    return ''.join(out)


@app.get("/api/tts")
def text_to_speech(text: str, language: str = "en"):
    """
    Generate Text-to-Speech audio stream (MP3) for health answers.
    Fully supports English (en), Hindi (hi), Odia (or), Bengali (bn), Telugu (te), and Tamil (ta).
    """
    if not text or not text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty for TTS synthesis.")

    import re
    import hashlib
    import io
    # Clean markdown formatting, bold/italics, and URLs for clean acoustic synthesis
    cleaned = re.sub(r"\[.*?\]\(.*?\)", "", text)
    cleaned = re.sub(r"[\*\#\_\`\>\[\]]", "", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()[:800]

    if not cleaned:
        raise HTTPException(status_code=400, detail="No readable text after cleanup.")

    cache_key = f"{language}_{hashlib.md5(cleaned.encode('utf-8')).hexdigest()}"
    if cache_key in _tts_audio_cache:
        return StreamingResponse(
            io.BytesIO(_tts_audio_cache[cache_key]),
            media_type="audio/mpeg",
            headers={
                "Content-Disposition": f"inline; filename=health_speech_{language}.mp3",
                "X-TTS-Language": language,
                "Cache-Control": "public, max-age=86400",
            },
        )

    try:
        from gtts import gTTS

        if language == "or":
            phonetic_text = odia_to_phonetic_devanagari(cleaned)
            tts = gTTS(text=phonetic_text, lang="hi")
            tts_lang = "or"
        elif language in {"hi", "bn", "te", "ta"}:
            tts = gTTS(text=cleaned, lang=language)
            tts_lang = language
        else:
            tts = gTTS(text=cleaned, lang="en")
            tts_lang = "en"

        fp = io.BytesIO()
        tts.write_to_fp(fp)
        audio_bytes = fp.getvalue()
        fp.seek(0)

        # Store in LRU cache
        if len(_tts_audio_cache) > 500:
            _tts_audio_cache.pop(next(iter(_tts_audio_cache)))
        _tts_audio_cache[cache_key] = audio_bytes

        return StreamingResponse(
            fp,
            media_type="audio/mpeg",
            headers={
                "Content-Disposition": f"inline; filename=health_speech_{tts_lang}.mp3",
                "X-TTS-Language": tts_lang,
                "Cache-Control": "public, max-age=86400",
            },
        )
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"TTS synthesis temporarily unavailable: {str(e)}",
        )

