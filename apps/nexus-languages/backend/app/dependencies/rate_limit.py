"""Dependency helpers for rate limiting."""

from functools import lru_cache

from ..core.config import get_settings
from ..services.rate_limit import RateLimitRule, RateLimiter


@lru_cache(maxsize=1)
def _cached_rate_limiter() -> RateLimiter:
    settings = get_settings()

    rules: list[RateLimitRule] = []
    if settings.rate_limit_enabled:
        if settings.rate_limit_hourly_quota > 0:
            rules.append(
                RateLimitRule(
                    name="hourly",
                    key="hour",
                    max_requests=settings.rate_limit_hourly_quota,
                    window_seconds=settings.rate_limit_hourly_window_seconds,
                    error_message_template=
                    "Has alcanzado el límite de {limit} análisis por hora. Inténtalo de nuevo en {retry_minutes} minutos.",
                )
            )
        if settings.rate_limit_daily_quota > 0:
            rules.append(
                RateLimitRule(
                    name="daily",
                    key="day",
                    max_requests=settings.rate_limit_daily_quota,
                    window_seconds=settings.rate_limit_daily_window_seconds,
                    error_message_template=
                    "Llegaste al máximo diario de {limit} análisis. Vuelve en {retry_hours} horas o mañana.",
                )
            )

    return RateLimiter(rules=rules, enabled=settings.rate_limit_enabled)


def get_rate_limiter() -> RateLimiter:
    """Return the shared rate limiter instance."""

    return _cached_rate_limiter()


def reset_rate_limiter_cache() -> None:
    """Clear cached state for test environments or manual resets."""

    limiter = _cached_rate_limiter()
    limiter.clear()
