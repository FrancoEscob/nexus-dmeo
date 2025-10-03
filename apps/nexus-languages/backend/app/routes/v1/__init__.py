"""Version 1 API routes."""

from fastapi import APIRouter

from .locales import router as locales_router
from .rate_limit import router as rate_limit_router
from .status import router as status_router
from .assess import router as assess_router


router = APIRouter(prefix="/v1")
router.include_router(status_router)
router.include_router(locales_router)
router.include_router(rate_limit_router)
router.include_router(assess_router)

__all__ = ["router"]
