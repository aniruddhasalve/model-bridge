from typing import Any, Literal
from pydantic import BaseModel, Field


class TextInput(BaseModel):
    text: str = Field(min_length=1)


class ChatInput(BaseModel):
    messages: list[dict[str, str]] = Field(min_length=1)
    temperature: float = Field(default=0.2, ge=0, le=2)


class ClassifyInput(TextInput):
    labels: list[str] = Field(min_length=1, max_length=50)


class ExtractInput(TextInput):
    fields: list[str] = Field(min_length=1, max_length=50)


class ModelResponse(BaseModel):
    provider: str
    model: str
    result: Any
    usage: dict[str, int] = Field(default_factory=dict)


class HealthResponse(BaseModel):
    status: Literal["ok"]
    provider: str
    mode: str
