"""Tests for the mock pronunciation assessment endpoint."""

from __future__ import annotations

import io
import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from fastapi.testclient import TestClient

from app.main import app


API_PATH = "/api/v1/assess/pronunciation"


class AssessMockTests(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_assess_with_webm_like_bytes_returns_ok(self) -> None:
        # Use arbitrary bytes and content type webm so server doesn't try WAV parsing
        audio_bytes = b"\x1aE\xdf\xa3webm-opus-bytes"
        files = {
            "audio": ("sample.webm", io.BytesIO(audio_bytes), "audio/webm"),
        }
        data = {
            "targetLocale": "en-US",
            "referenceText": "hello there",
            "uiLocale": "en",
            "durationMs": 2500,
        }
        r = self.client.post(API_PATH, files=files, data=data, headers={"User-Agent": "pytest"})
        self.assertEqual(r.status_code, 200, r.text)
        body = r.json()
        self.assertIn("scores", body)
        self.assertIn("feedback", body)
        self.assertEqual(body["metadata"]["engine"], "mock")

    def test_duration_limit_returns_413(self) -> None:
        audio_bytes = b"x" * 128
        files = {"audio": ("sample.webm", io.BytesIO(audio_bytes), "audio/webm")}
        data = {
            "targetLocale": "es-ES",
            "referenceText": "hola",
            "uiLocale": "es",
            "durationMs": 20000,  # 20s, above 10s cap
        }
        r = self.client.post(API_PATH, files=files, data=data)
        self.assertEqual(r.status_code, 413)


if __name__ == "__main__":
    unittest.main()
