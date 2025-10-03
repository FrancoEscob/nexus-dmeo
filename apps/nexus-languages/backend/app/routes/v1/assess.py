"""Pronunciation assessment endpoint (mock-first)."""

from __future__ import annotations

import io
import struct
from typing import Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, UploadFile, status

from ...core.config import get_settings
from ...dependencies.rate_limit import get_rate_limiter
from ...schemas.assessment import AssessmentResponse
from ...services import RateLimiter
from ...services.assessment_mock import mock_assess
from ...services.azure_assessment import azure_assess


router = APIRouter(prefix="/assess", tags=["assessment"])


def _parse_wav_duration_ms(data: bytes) -> Optional[int]:
    # Minimal WAV header parsing to estimate duration.
    try:
        bio = io.BytesIO(data)
        riff = bio.read(12)
        if len(riff) < 12 or riff[:4] != b"RIFF" or riff[8:12] != b"WAVE":
            return None
        fmt_chunk_found = False
        num_channels = sample_rate = bits_per_sample = 0
        data_size = 0
        while True:
            header = bio.read(8)
            if len(header) < 8:
                break
            chunk_id, chunk_size = struct.unpack('<4sI', header)
            chunk_id = chunk_id.decode('ascii', errors='ignore')
            if chunk_id == 'fmt ':
                fmt_chunk_found = True
                fmt = bio.read(chunk_size)
                if len(fmt) >= 16:
                    _, num_channels, sample_rate, _, _, bits_per_sample = struct.unpack('<HHIIHH', fmt[:16])
                else:
                    return None
            elif chunk_id == 'data':
                data_size = chunk_size
                bio.seek(chunk_size, io.SEEK_CUR)
            else:
                bio.seek(chunk_size, io.SEEK_CUR)
        if not fmt_chunk_found or not sample_rate or not bits_per_sample or not num_channels:
            return None
        bytes_per_sample = bits_per_sample // 8
        if bytes_per_sample == 0:
            return None
        total_samples = data_size // (num_channels * bytes_per_sample)
        duration_sec = total_samples / float(sample_rate)
        return int(duration_sec * 1000)
    except Exception:
        return None


def _enforce_duration_or_413(*, data: bytes, content_type: str, ui_duration_ms: Optional[int], max_seconds: int) -> int | None:
    max_ms = max_seconds * 1000
    if ui_duration_ms and ui_duration_ms > max_ms:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail={"code": "AUDIO_TOO_LONG", "message": f"Audio exceeds {max_seconds}s limit."},
        )
    if content_type and "wav" in content_type:
        wav_ms = _parse_wav_duration_ms(data)
        if wav_ms and wav_ms > max_ms:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail={"code": "AUDIO_TOO_LONG", "message": f"Audio exceeds {max_seconds}s limit."},
            )
        return wav_ms
    return ui_duration_ms


@router.post("/pronunciation", response_model=AssessmentResponse)
async def assess_pronunciation(
    request: Request,
    audio: UploadFile = File(..., description="Audio file ≤10s (webm/opus or wav)"),
    targetLocale: str = Form(...),
    referenceText: str = Form(...),
    uiLocale: str = Form("en"),
    nativeLanguage: str | None = Form(None),
    durationMs: int | None = Form(default=None, description="Optional duration hint from UI in ms"),
    limiter: RateLimiter = Depends(get_rate_limiter),
) -> AssessmentResponse:
    """Assess pronunciation quality for a short audio snippet.

    Rate-limited; supports mock mode by default. Enforces a 10s cap using
    UI-provided duration and best-effort WAV parsing.
    """

    settings = get_settings()

    outcome = limiter.hit(
        request,
        target_locale=targetLocale,
        target_language=nativeLanguage,
    )
    _ = outcome  # counted for quota; details are not returned here

    data = await audio.read()

    est_ms = _enforce_duration_or_413(
        data=data,
        content_type=audio.content_type or "",
        ui_duration_ms=durationMs,
        max_seconds=settings.max_audio_seconds,
    )

    if settings.assess_mode == "mock":
        return mock_assess(
            audio_bytes=data,
            target_locale=targetLocale,
            reference_text=referenceText,
            duration_ms=est_ms,
        )

    # Azure (not yet implemented):
    return await azure_assess(
        audio_bytes=data,
        content_type=audio.content_type or "application/octet-stream",
        target_locale=targetLocale,
        reference_text=referenceText,
        duration_ms=est_ms,
    )


__all__ = ["router"]
