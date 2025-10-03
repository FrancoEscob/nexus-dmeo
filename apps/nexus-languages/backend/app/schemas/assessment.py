"""Pydantic models for pronunciation assessment API."""

from __future__ import annotations

from typing import List, Literal, Optional

from pydantic import BaseModel, Field


class WordTiming(BaseModel):
    start: int = Field(description="Start time in milliseconds")
    end: int = Field(description="End time in milliseconds")


class WordResult(BaseModel):
    text: str
    accuracy: int = Field(ge=0, le=100)
    timing: Optional[WordTiming] = None


class AssessmentScores(BaseModel):
    overall: int = Field(ge=0, le=100)
    accuracy: int = Field(ge=0, le=100)
    fluency: int = Field(ge=0, le=100)
    completeness: int = Field(ge=0, le=100)
    prosody: int = Field(ge=0, le=100)


class FeedbackCard(BaseModel):
    title: str
    body: str
    type: Literal["tip", "info", "warning"] = "tip"


class AssessmentMetadata(BaseModel):
    engine: str = Field(description="mock | azure")
    duration_ms: int | None = None
    locale: str | None = None


class AssessmentResponse(BaseModel):
    scores: AssessmentScores
    words: List[WordResult] = []
    feedback: List[FeedbackCard] = []
    metadata: AssessmentMetadata


__all__ = [
    "WordTiming",
    "WordResult",
    "AssessmentScores",
    "FeedbackCard",
    "AssessmentMetadata",
    "AssessmentResponse",
]
