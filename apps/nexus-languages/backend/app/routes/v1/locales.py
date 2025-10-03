"""Azure locales endpoints."""

from __future__ import annotations

from typing import Iterable

from fastapi import APIRouter, Query

from ...schemas.locales import AzureLocale
from ...services import get_available_locales


router = APIRouter(prefix="/locales", tags=["locales"])


def _apply_filters(
    locales: Iterable[AzureLocale],
    target_locale: str | None,
    target_language: str | None,
) -> list[AzureLocale]:
    results: list[AzureLocale] = []
    for locale in locales:
        if target_locale and locale.target_locale.lower() != target_locale.lower():
            continue
        if target_language and locale.target_language.lower() != target_language.lower():
            continue
        results.append(locale)
    return results


@router.get("", response_model=list[AzureLocale])
async def list_locales(
    target_locale: str | None = Query(
        default=None,
        description="Filter by Azure locale code (e.g. en-US)",
        alias="targetLocale",
    ),
    target_language: str | None = Query(
        default=None,
        description="Filter by language family (e.g. English)",
        alias="targetLanguage",
    ),
) -> list[AzureLocale]:
    """Return cached Azure pronunciation locales with optional filtering."""

    locales = get_available_locales()
    filtered = _apply_filters(locales, target_locale, target_language)
    return list(filtered or locales)
