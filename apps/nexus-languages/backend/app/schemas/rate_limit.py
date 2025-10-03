"""Schemas for rate limit endpoints."""

from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field

from ..services.rate_limit import RateLimitRuleResult


class RateLimitProbeRequest(BaseModel):
    """Payload accepted by the probe endpoint to simulate an analysis."""

    target_locale: str | None = Field(default=None, alias="targetLocale")
    target_language: str | None = Field(default=None, alias="targetLanguage")

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {"targetLocale": "es-ES", "targetLanguage": "Spanish"}
        },
    }


class RateLimitProbeResponse(BaseModel):
    """Simple response summarizing available quota by rule."""

    message: str
    rules: List[RateLimitRuleResult]


__all__ = ["RateLimitProbeRequest", "RateLimitProbeResponse"]
