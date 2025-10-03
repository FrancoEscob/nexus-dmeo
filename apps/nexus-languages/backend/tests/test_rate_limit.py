"""Unit tests for the rate limiter probe endpoint."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from fastapi.testclient import TestClient

from app.dependencies.rate_limit import reset_rate_limiter_cache
from app.main import app


API_PATH = "/api/v1/rate-limit/probe"


class RateLimitProbeTests(unittest.TestCase):
    """Verify hourly quota enforcement and reset behaviour."""

    def setUp(self) -> None:
        reset_rate_limiter_cache()
        self.headers = {
            "User-Agent": "pytest-agent",
            "X-Forwarded-For": "203.0.113.10",
        }
        self.payload = {"targetLocale": "es-ES", "targetLanguage": "Spanish"}

    def test_within_quota_returns_remaining_budget(self) -> None:
        with TestClient(app) as client:
            response = client.post(API_PATH, json=self.payload, headers=self.headers)
            self.assertEqual(response.status_code, 200)
            body = response.json()
            self.assertEqual(body["message"], "Quota disponible")
            hourly_rule = next(rule for rule in body["rules"] if rule["name"] == "hourly")
            self.assertEqual(hourly_rule["limit"], 5)
            self.assertEqual(hourly_rule["remaining"], 4)

    def test_exceeding_hourly_quota_returns_429(self) -> None:
        with TestClient(app) as client:
            for _ in range(5):
                response = client.post(API_PATH, json=self.payload, headers=self.headers)
                self.assertEqual(response.status_code, 200)

            blocked = client.post(API_PATH, json=self.payload, headers=self.headers)
            self.assertEqual(blocked.status_code, 429)
            detail = blocked.json()["detail"]
            self.assertEqual(detail["code"], "RATE_LIMIT_EXCEEDED")
            self.assertEqual(detail["rule"], "hourly")
            self.assertEqual(detail["limit"], 5)

    def test_reset_rate_limiter_clears_state(self) -> None:
        with TestClient(app) as client:
            for _ in range(5):
                client.post(API_PATH, json=self.payload, headers=self.headers)

            blocked = client.post(API_PATH, json=self.payload, headers=self.headers)
            self.assertEqual(blocked.status_code, 429)

        reset_rate_limiter_cache()

        with TestClient(app) as client:
            response = client.post(API_PATH, json=self.payload, headers=self.headers)
            self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
