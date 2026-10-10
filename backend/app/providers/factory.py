from fastapi import HTTPException

from app.config import settings
from .mock import MockProvider
from .openai_compatible import OpenAICompatibleProvider


def get_provider():
    if settings.provider == "mock":
        return MockProvider()
    if settings.provider in {"openai", "openai-compatible"}:
        return OpenAICompatibleProvider()
    raise HTTPException(status_code=500, detail=f"Unsupported provider: {settings.provider}")
