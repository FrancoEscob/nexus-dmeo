"""Mock implementation for pronunciation assessment.

Generates deterministic but friendly scores and feedback based on the
reference text length and characters. Suitable for local dev and tests.
"""

from __future__ import annotations

from typing import List

from ..schemas.assessment import (
    AssessmentMetadata,
    AssessmentResponse,
    AssessmentScores,
    FeedbackCard,
    WordResult,
)


def _score_from_text(text: str) -> int:
    text = (text or "").strip()
    base = 75
    if not text:
        return base
    vowels = sum(1 for c in text.lower() if c in "aeiouáéíóúü")
    consonants = sum(1 for c in text.lower() if c.isalpha()) - vowels
    length_factor = min(10, max(0, len(text) // 10))
    variability = (vowels * 3 + consonants * 2 + length_factor) % 21  # 0..20
    return max(60, min(95, base + variability - 5))


def mock_assess(
    *,
    audio_bytes: bytes,
    target_locale: str,
    reference_text: str,
    duration_ms: int | None,
) -> AssessmentResponse:
    overall = _score_from_text(reference_text)
    accuracy = max(55, min(98, overall + 3))
    fluency = max(50, min(95, overall - 2))
    completeness = max(60, min(99, overall + 4))
    prosody = max(50, min(95, overall - 5))

    words: List[WordResult] = []
    offset = 0
    for token in (reference_text or "").split():
        w_score = max(50, min(99, _score_from_text(token)))
        start = offset
        dur = 200 + (len(token) % 4) * 80
        end = start + dur
        offset = end + 60
        words.append(
            WordResult(text=token.strip(",.!?;:"), accuracy=w_score, timing={"start": start, "end": end})
        )

    feedback = [
        FeedbackCard(
            title="Buen ritmo" if target_locale.startswith("es") else "Nice pacing",
            body=(
                "Mantén frases cortas y claras; respira entre ideas."
                if target_locale.startswith("es")
                else "Keep sentences short and clear; take small pauses between ideas."
            ),
            type="tip",
        ),
        FeedbackCard(
            title="Articulación" if target_locale.startswith("es") else "Articulation",
            body=(
                "Marca consonantes finales como /t/ y /d/ para ganar precisión."
                if target_locale.startswith("es")
                else "Enunciate final consonants like /t/ and /d/ to improve accuracy."
            ),
            type="tip",
        ),
    ]

    return AssessmentResponse(
        scores=AssessmentScores(
            overall=overall,
            accuracy=accuracy,
            fluency=fluency,
            completeness=completeness,
            prosody=prosody,
        ),
        words=words,
        feedback=feedback,
        metadata=AssessmentMetadata(engine="mock", duration_ms=duration_ms or 0, locale=target_locale),
    )


__all__ = ["mock_assess"]
