"""Status endpoints for API version 1."""

from datetime import datetime

from fastapi import APIRouter


router = APIRouter(tags=["status"])


@router.get("/status")
async def get_status() -> dict:
    """Return service status and timestamp."""

    return {
        "service": "nexus-languages-backend",
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat(),
    }
