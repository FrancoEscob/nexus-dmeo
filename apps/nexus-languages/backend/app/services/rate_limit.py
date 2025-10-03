"""Rate limiting utilities for the pronunciation API."""

from __future__ import annotations

import math
import time
from dataclasses import dataclass
from typing import Dict, List

from fastapi import HTTPException, Request, status
from pydantic import BaseModel, Field


@dataclass(frozen=True)
class RateLimitRule:
    """Configuration for a rate limit window."""

    name: str
    key: str
    max_requests: int
    window_seconds: int
    error_message_template: str


class RateLimitRuleResult(BaseModel):
    """State returned after a successful rate limit check."""

    name: str
    limit: int
    window_seconds: int
    remaining: int
    retry_after_seconds: int


class RateLimitOutcome(BaseModel):
    """Outcome of processing a rate limit hit."""

    allowed: bool = Field(default=True)
    rules: List[RateLimitRuleResult] = Field(default_factory=list)


class RateLimitIdentity(BaseModel):
    """Identity tuple used for rate limiting buckets."""

    ip_address: str
    user_agent: str
    target_locale: str | None = None
    target_language: str | None = None

    def cache_key(self) -> str:
        parts: List[str] = [self.ip_address or "unknown", self.user_agent or "unknown"]
        if self.target_locale:
            parts.append(self.target_locale.lower())
        if self.target_language:
            parts.append(self.target_language.lower())
        return "|".join(parts)

    @classmethod
    def from_request(
        cls,
        request: Request,
        *,
        target_locale: str | None = None,
        target_language: str | None = None,
    ) -> "RateLimitIdentity":
        forwarded_for = request.headers.get("x-forwarded-for") or request.headers.get("X-Forwarded-For")
        if forwarded_for:
            ip_address = forwarded_for.split(",")[0].strip()
        elif request.client and request.client.host:
            ip_address = request.client.host
        else:
            ip_address = "unknown"

        user_agent = request.headers.get("user-agent") or request.headers.get("User-Agent") or "unknown"
        user_agent = user_agent[:120]

        return cls(
            ip_address=ip_address,
            user_agent=user_agent,
            target_locale=target_locale,
            target_language=target_language,
        )


class MemoryRateLimitStore:
    """Simple in-memory store for request timestamps."""

    def __init__(self) -> None:
        self._records: Dict[str, List[float]] = {}

    def increment(self, key: str, window_seconds: int, now: float) -> tuple[int, float]:
        bucket = self._records.setdefault(key, [])
        cutoff = now - window_seconds

        # Remove entries that are outside the window
        while bucket and bucket[0] <= cutoff:
            bucket.pop(0)

        bucket.append(now)
        count = len(bucket)
        retry_after = 0.0
        if bucket:
            retry_after = max(0.0, window_seconds - (now - bucket[0]))

        return count, retry_after

    def clear(self) -> None:
        self._records.clear()


class RateLimiter:
    """Small rate limiter with pluggable store."""

    def __init__(
        self,
        *,
        rules: List[RateLimitRule],
        enabled: bool = True,
        store: MemoryRateLimitStore | None = None,
    ) -> None:
        self.rules = [rule for rule in rules if rule.max_requests > 0]
        self.enabled = enabled and bool(self.rules)
        self.store = store or MemoryRateLimitStore()

    def clear(self) -> None:
        self.store.clear()

    def hit(
        self,
        request: Request,
        *,
        target_locale: str | None = None,
        target_language: str | None = None,
    ) -> RateLimitOutcome:
        if not self.enabled:
            return RateLimitOutcome(allowed=True, rules=[])

        identity = RateLimitIdentity.from_request(
            request,
            target_locale=target_locale,
            target_language=target_language,
        )
        now = time.time()
        results: List[RateLimitRuleResult] = []

        for rule in self.rules:
            key = f"{rule.key}:{identity.cache_key()}"
            count, retry_after = self.store.increment(key, rule.window_seconds, now)
            remaining = max(0, rule.max_requests - count)
            retry_seconds = int(math.ceil(retry_after))

            if count > rule.max_requests:
                retry_minutes = max(1, math.ceil(retry_after / 60))
                retry_hours = retry_after / 3600
                detail_message = rule.error_message_template.format(
                    limit=rule.max_requests,
                    window_minutes=max(1, rule.window_seconds // 60),
                    retry_minutes=retry_minutes,
                    retry_hours=max(1, round(max(retry_hours, retry_minutes / 60), 1)),
                )

                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail={
                        "code": "RATE_LIMIT_EXCEEDED",
                        "message": detail_message,
                        "rule": rule.name,
                        "limit": rule.max_requests,
                        "window_seconds": rule.window_seconds,
                        "retry_after_seconds": retry_seconds,
                    },
                    headers={"Retry-After": str(max(1, retry_seconds))},
                )

            results.append(
                RateLimitRuleResult(
                    name=rule.name,
                    limit=rule.max_requests,
                    window_seconds=rule.window_seconds,
                    remaining=remaining,
                    retry_after_seconds=retry_seconds,
                )
            )

        return RateLimitOutcome(allowed=True, rules=results)


__all__ = [
    "RateLimitRule",
    "RateLimitRuleResult",
    "RateLimitOutcome",
    "RateLimitIdentity",
    "RateLimiter",
]
