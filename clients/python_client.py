from __future__ import annotations

from typing import Any
import httpx


class ModelBridgeClient:
    def __init__(self, base_url: str, api_key: str, timeout: float = 45):
        self.base_url = base_url.rstrip("/")
        self.client = httpx.Client(timeout=timeout, headers={"Authorization": f"Bearer {api_key}"})

    def _post(self, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        response = self.client.post(f"{self.base_url}{path}", json=payload)
        response.raise_for_status()
        return response.json()

    def chat(self, messages: list[dict[str, str]]) -> dict[str, Any]:
        return self._post("/v1/chat", {"messages": messages})

    def classify(self, text: str, labels: list[str]) -> dict[str, Any]:
        return self._post("/v1/classify", {"text": text, "labels": labels})

    def extract(self, text: str, fields: list[str]) -> dict[str, Any]:
        return self._post("/v1/extract", {"text": text, "fields": fields})

    def summarize(self, text: str) -> dict[str, Any]:
        return self._post("/v1/summarize", {"text": text})
