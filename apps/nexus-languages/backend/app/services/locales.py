"""Utility helpers for working with Azure locale metadata."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Iterable, List

from fastapi import HTTPException, status

from ..schemas.locales import AzureLocale


DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "azure_locales.json"


def _load_raw_records(data_path: Path = DATA_FILE) -> Iterable[dict]:
    if not data_path.exists():
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Azure locales data file is missing. Run scripts/fetch_azure_locales.py first.",
        )

    with data_path.open("r", encoding="utf-8") as handle:
        try:
            payload = json.load(handle)
        except json.JSONDecodeError as exc:  # pragma: no cover - defensive branch
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Invalid locales data file: {exc.msg}",
            ) from exc

    if not isinstance(payload, list):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Azure locales payload must be a list",
        )

    return payload


@lru_cache
def get_available_locales(data_path: Path = DATA_FILE) -> tuple[AzureLocale, ...]:
    """Return cached locales parsed from the JSON bundle."""

    records = _load_raw_records(data_path=data_path)
    locales: List[AzureLocale] = [AzureLocale.model_validate(item) for item in records]
    locales.sort(key=lambda record: record.target_display_name.lower())
    return tuple(locales)


def refresh_available_locales(data_path: Path = DATA_FILE) -> tuple[AzureLocale, ...]:
    """Clear cache so subsequent calls reflect the latest JSON on disk."""

    get_available_locales.cache_clear()  # type: ignore[attr-defined]
    return get_available_locales(data_path=data_path)


__all__ = ["get_available_locales", "refresh_available_locales"]
