from __future__ import annotations

import httpx
from fastapi import HTTPException

from app.config import settings
from app.schemas import ChatInput, ClassifyInput, ExtractInput, ModelResponse, TextInput


class OpenAICompatibleProvider:
    name = "openai-compatible"
    model = settings.provider_model or "default"

    async def _complete(self, messages: list[dict[str, str]], operation: str) -> ModelResponse:
        if not settings.provider_base_url or not settings.provider_api_key:
            raise HTTPException(status_code=503, detail="Provider credentials are not configured")
        url = settings.provider_base_url.rstrip("/") + "/chat/completions"
        headers = {"Authorization": f"Bearer {settings.provider_api_key}"}
        payload = {"model": self.model, "messages": messages, "temperature": 0.2}
        try:
            async with httpx.AsyncClient(timeout=45) as client:
                response = await client.post(url, headers=headers, json=payload)
                response.raise_for_status()
        except httpx.HTTPError as exc:
            raise HTTPException(status_code=502, detail=f"Model provider request failed: {exc.__class__.__name__}") from exc
        data = response.json()
        usage = data.get("usage", {})
        result = data.get("choices", [{}])[0].get("message", {}).get("content", "")
        return ModelResponse(provider=self.name, model=self.model, result={"operation": operation, "content": result}, usage={key: int(value) for key, value in usage.items() if isinstance(value, int)})

    async def chat(self, request: ChatInput) -> ModelResponse:
        return await self._complete(request.messages, "chat")

    async def classify(self, request: ClassifyInput) -> ModelResponse:
        prompt = f"Classify this text into exactly one of these labels: {request.labels}. Return JSON with label and confidence. Text: {request.text}"
        return await self._complete([{"role": "user", "content": prompt}], "classify")

    async def extract(self, request: ExtractInput) -> ModelResponse:
        prompt = f"Extract these fields as JSON: {request.fields}. Text: {request.text}"
        return await self._complete([{"role": "user", "content": prompt}], "extract")

    async def summarize(self, request: TextInput) -> ModelResponse:
        return await self._complete([{"role": "user", "content": f"Summarize this text clearly: {request.text}"}], "summarize")
