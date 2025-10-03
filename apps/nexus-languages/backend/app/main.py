"""FastAPI application entrypoint for Nexus Languages."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.config import get_settings
from .routes import router as api_router


def create_app() -> FastAPI:
    """Instantiate and configure the FastAPI application."""

    settings = get_settings()
    app = FastAPI(title=settings.app_name, debug=settings.debug)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=list(settings.allowed_origins),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router)

    @app.get("/health", tags=["health"])
    async def health_check():
        """Simple health check endpoint."""

        return {"status": "ok"}

    return app


app = create_app()
