from __future__ import annotations

from typing import Protocol

from app.schemas import ChatInput, ClassifyInput, ExtractInput, ModelResponse, TextInput


class Provider(Protocol):
    name: str

    async def chat(self, request: ChatInput) -> ModelResponse: ...
    async def classify(self, request: ClassifyInput) -> ModelResponse: ...
    async def extract(self, request: ExtractInput) -> ModelResponse: ...
    async def summarize(self, request: TextInput) -> ModelResponse: ...
