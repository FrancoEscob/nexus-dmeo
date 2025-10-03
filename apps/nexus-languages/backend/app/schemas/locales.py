"""Pydantic schemas for Azure locale metadata."""

from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field


class NativeLocale(BaseModel):
    """Represents a native locale option the learner can choose."""

    locale: str = Field(..., description="Locale code, e.g. en-US or es-ES")
    display_name: str = Field(..., description="Human-friendly native locale name")


class VoiceSample(BaseModel):
    """Voice metadata to showcase available Azure voices for the locale."""

    short_name: str = Field(..., description="Azure short name, e.g. en-US-JennyNeural")
    display_name: str = Field(..., description="Friendly voice name presented to users")
    gender: str | None = Field(default=None, description="Voice gender as reported by Azure")


class AzureLocale(BaseModel):
    """Aggregated information about a pronunciation-assessment target locale."""

    target_locale: str = Field(..., description="Azure locale for assessment, e.g. en-US")
    target_language: str = Field(..., description="Language family, e.g. English")
    target_display_name: str = Field(..., description="Localized language + region label")
    native_locales: List[NativeLocale] = Field(default_factory=list, description="Suggested native locales")
    voices: List[VoiceSample] = Field(default_factory=list, description="Sample of supported Neural voices")

    model_config = {
        "json_schema_extra": {
            "example": {
                "target_locale": "en-US",
                "target_language": "English",
                "target_display_name": "English (United States)",
                "native_locales": [
                    {"locale": "en-US", "display_name": "English (United States)"},
                    {"locale": "es-ES", "display_name": "Español (España)"},
                ],
                "voices": [
                    {"short_name": "en-US-JennyNeural", "display_name": "Jenny", "gender": "Female"},
                    {"short_name": "en-US-GuyNeural", "display_name": "Guy", "gender": "Male"},
                ],
            }
        }
    }


__all__ = ["AzureLocale", "NativeLocale", "VoiceSample"]
