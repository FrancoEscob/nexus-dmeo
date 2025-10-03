#!/usr/bin/env python3
"""Fetch Azure Speech locales/voices and export them as JSON.

This utility hits the Text-to-Speech voices endpoint to build a condensed
dataset consumable by the `/api/v1/locales` FastAPI route.

Usage example:

    python scripts/fetch_azure_locales.py \
        --region eastus \
        --subscription-key "$AZURE_SPEECH_KEY" \
        --output app/data/azure_locales.json

The resulting JSON groups voices by locale and captures a small sample of
voices plus suggested native locales (initially defaulting to the same
locale). You can manually edit the native locale suggestions afterward to
better reflect accent guidance.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List

import httpx


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download Azure Speech locales")
    parser.add_argument("--region", required=True, help="Azure Speech region, e.g. eastus")
    parser.add_argument(
        "--subscription-key",
        default=os.environ.get("AZURE_SPEECH_KEY"),
        help="Azure Speech key (default: AZURE_SPEECH_KEY env)",
    )
    parser.add_argument(
        "--output",
        default="app/data/azure_locales.json",
        help="Path to write JSON bundle",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=20.0,
        help="HTTP timeout in seconds",
    )
    args = parser.parse_args()

    if not args.subscription_key:
        parser.error("You must provide --subscription-key or set AZURE_SPEECH_KEY")

    return args


async def fetch_voices(region: str, key: str, timeout: float) -> list[dict[str, Any]]:
    url = f"https://{region}.tts.speech.microsoft.com/cognitiveservices/voices/list"
    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "User-Agent": "nexus-languages-fetch-locales/1.0",
    }

    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        return response.json()


def build_dataset(voices: Iterable[Dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: Dict[str, Dict[str, Any]] = defaultdict(
        lambda: {
            "target_locale": "",
            "target_language": "",
            "target_display_name": "",
            "native_locales": [],
            "voices": [],
        }
    )

    for voice in voices:
        locale = voice.get("Locale")
        if not locale:
            continue

        entry = grouped[locale]
        entry["target_locale"] = locale
        entry["target_display_name"] = voice.get("LocaleName", locale)
        entry["target_language"] = voice.get("LocaleName", locale).split("(")[0].strip()

        # ensure we store at least one native locale suggestion
        if not entry["native_locales"]:
            local_name = voice.get("LocaleName") or locale
            entry["native_locales"].append({"locale": locale, "display_name": local_name})

        entry["voices"].append(
            {
                "short_name": voice.get("ShortName", ""),
                "display_name": voice.get("DisplayName", voice.get("ShortName", "")),
                "gender": voice.get("Gender"),
            }
        )

    dataset = list(grouped.values())

    # Deduplicate voices and sort for deterministic output
    for entry in dataset:
        seen = {}
        deduped: List[dict[str, Any]] = []
        for voice in entry["voices"]:
            key = voice.get("short_name")
            if key and key in seen:
                continue
            if key:
                seen[key] = True
            deduped.append(voice)
        entry["voices"] = sorted(deduped, key=lambda item: item.get("display_name", "").lower())

    dataset.sort(key=lambda item: item["target_display_name"].lower())
    return dataset


async def main() -> None:
    args = parse_args()
    voices = await fetch_voices(args.region, args.subscription_key, args.timeout)
    dataset = build_dataset(voices)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(dataset, handle, ensure_ascii=False, indent=2)

    print(f"Saved {len(dataset)} locales to {output_path}")


if __name__ == "__main__":
    asyncio.run(main())
