"""FastAPI Application for Multilingual Health FAQ Assistant."""
from fastapi import FastAPI, HTTPException, Request, Depends, status
from fastapi.middleware.cors import CORSMiddleware
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
            with open(config_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                _LANGUAGES_REGISTRY = {l["code"]: l for l in data.get("languages", [])}

    return _VECTOR_STORE, _GUARDRAIL, _GENERATOR, _LANGUAGES_REGISTRY


from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    get_services()
    yield

app = FastAPI(
    title="Multilingual Health FAQ Assistant API",
    description="Grounded health question answering in Indian languages (Hindi, Odia, English) with verifiable citations and strict safety guardrails.",
    version="1.0.0",
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
        version="1.0.0",
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
    results = store.search(req.question, top_k=5)

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

    return AskResponse(
        answer=gen_result.answer,
        language=gen_result.language,
        status=gen_result.status,  # type: ignore
        citations=citation_items,
        disclaimer=gen_result.disclaimer,
        request_id=gen_result.request_id,
        is_experimental=is_experimental,
    )


@app.post("/api/feedback", response_model=FeedbackResponse)
def submit_feedback(req: FeedbackRequest):
    """Store thumbs up / down rating and comment."""
    save_feedback(req.request_id, req.rating, req.comment)
    return FeedbackResponse(
        status="success",
        message="Feedback successfully recorded.",
    )
