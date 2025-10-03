"""Endpoints related to rate limit diagnostics."""

from __future__ import annotations

from fastapi import APIRouter, Body, Depends, Request

from ...dependencies.rate_limit import get_rate_limiter
from ...schemas.rate_limit import RateLimitProbeRequest, RateLimitProbeResponse
from ...services import RateLimiter


router = APIRouter(prefix="/rate-limit", tags=["rate-limit"])


@router.post("/probe", response_model=RateLimitProbeResponse)
async def rate_limit_probe(
    request: Request,
    payload: RateLimitProbeRequest | None = Body(default=None),
    limiter: RateLimiter = Depends(get_rate_limiter),
) -> RateLimitProbeResponse:
    """Check the current rate limit budget for the caller."""

    payload = payload or RateLimitProbeRequest()
    outcome = limiter.hit(
        request,
        target_locale=payload.target_locale,
        target_language=payload.target_language,
    )

    return RateLimitProbeResponse(
        message="Quota disponible",
        rules=outcome.rules,
    )
