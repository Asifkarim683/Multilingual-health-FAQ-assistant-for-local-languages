"""Pydantic schemas for the Health FAQ Assistant API."""
from pydantic import BaseModel, Field
from typing import List, Optional, Literal, Dict, Any


class AskRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=2,
        max_length=1000,
        description="User health question in English, Hindi, Odia, etc.",
        examples=["What are the early symptoms of dengue?"],
    )
    language: Optional[str] = Field(
        default="auto",
        description="Language code ('auto', 'en', 'hi', 'or', 'bn', 'te', 'ta')",
    )
    session_id: Optional[str] = Field(
        default=None,
        description="Optional session tracking identifier",
    )


class CitationItem(BaseModel):
    id: int
    title: str
    url: str
    section: str


class AskResponse(BaseModel):
    answer: str
    language: str
    status: Literal["answered", "refused", "emergency"]
    citations: List[CitationItem]
    disclaimer: str
    request_id: str
    is_experimental: bool = False
    corrected_query: Optional[str] = None


class FeedbackRequest(BaseModel):
    request_id: str = Field(..., description="ID of the question response being rated")
    rating: Literal["up", "down"] = Field(..., description="Thumbs up or down")
    comment: Optional[str] = Field(default=None, max_length=500, description="Optional text feedback")


class FeedbackResponse(BaseModel):
    status: str
    message: str


class HealthResponse(BaseModel):
    status: str
    version: str
    knowledge_base_version: str
    total_chunks: int
    supported_languages: List[str]


class LanguageInfo(BaseModel):
    code: str
    name: str
    native_name: str
    script: str
    font: str
    status: str
    example_questions: List[str]
    ui_strings: Dict[str, Any]
