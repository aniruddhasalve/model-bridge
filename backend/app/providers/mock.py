from app.schemas import ChatInput, ClassifyInput, ExtractInput, ModelResponse, TextInput


class MockProvider:
    name = "mock"
    model = "mock-v1"

    async def chat(self, request: ChatInput) -> ModelResponse:
        last = request.messages[-1].get("content", "")
        return ModelResponse(provider=self.name, model=self.model, result={"message": f"Mock response for: {last[:160]}"}, usage={"input_chars": len(last)})

    async def classify(self, request: ClassifyInput) -> ModelResponse:
        lowered = request.text.lower()
        selected = next((label for label in request.labels if label.lower() in lowered), request.labels[0])
        return ModelResponse(provider=self.name, model=self.model, result={"label": selected, "confidence": 0.5, "all_labels": request.labels}, usage={"input_chars": len(request.text)})

    async def extract(self, request: ExtractInput) -> ModelResponse:
        return ModelResponse(provider=self.name, model=self.model, result={field: None for field in request.fields}, usage={"input_chars": len(request.text)})

    async def summarize(self, request: TextInput) -> ModelResponse:
        words = request.text.split()
        summary = " ".join(words[:40]) + ("…" if len(words) > 40 else "")
        return ModelResponse(provider=self.name, model=self.model, result={"summary": summary}, usage={"input_chars": len(request.text)})
