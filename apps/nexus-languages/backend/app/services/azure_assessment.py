"""Azure Pronunciation Assessment integration (stub).

Wires up the REST API call in a future iteration. For now, raises a
controlled error if invoked while not implemented.
"""

from __future__ import annotations

from fastapi import HTTPException, status

from ..schemas.assessment import AssessmentResponse


async def azure_assess(
    *,
    audio_bytes: bytes,
    content_type: str,
    target_locale: str,
    reference_text: str,
    duration_ms: int | None,
) -> AssessmentResponse:
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail={
            "code": "AZURE_NOT_IMPLEMENTED",
            "message": "Azure assessment integration is not implemented yet.",
        },
    )


__all__ = ["azure_assess"]
