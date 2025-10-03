"""Application configuration and settings management."""

from functools import lru_cache
from typing import Sequence

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Base configuration for the FastAPI service."""

    app_name: str = Field(default="Nexus Languages API")
    debug: bool = Field(default=False)
    allowed_origins: Sequence[str] = Field(default_factory=lambda: ["http://localhost:3000"])
    rate_limit_enabled: bool = Field(default=True)
    rate_limit_hourly_quota: int = Field(default=5)
    rate_limit_hourly_window_seconds: int = Field(default=3600)
    rate_limit_daily_quota: int = Field(default=10)
    rate_limit_daily_window_seconds: int = Field(default=86400)
    # Assessment flow
    assess_mode: str = Field(default="mock", description="mock | azure")
    max_audio_seconds: int = Field(default=10)
    # Azure Speech
    azure_speech_key: str | None = Field(default=None)
    azure_speech_region: str | None = Field(default=None)
    # Gemini (optional)
    gemini_api_key: str | None = Field(default=None)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @field_validator("allowed_origins", mode="before")
    @classmethod
    def split_allowed_origins(cls, value: Sequence[str] | str) -> Sequence[str]:
        """Allow comma-separated origins in environment variables."""

        if isinstance(value, str):
            return tuple(o.strip() for o in value.split(",") if o.strip())
        return value


@lru_cache()
def get_settings() -> Settings:
    """Return a cached settings instance."""

    return Settings()
