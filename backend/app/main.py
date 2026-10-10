from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.providers.factory import get_provider
from app.schemas import ChatInput, ClassifyInput, ExtractInput, HealthResponse, ModelResponse, TextInput

app = FastAPI(title="ModelBridge API", version="0.1.0", description="Provider-neutral ML operations for web and backend projects.")
app.add_middleware(CORSMiddleware, allow_origins=settings.allowed_origins, allow_credentials=False, allow_methods=["GET", "POST"], allow_headers=["Authorization", "Content-Type"])


def require_api_key(authorization: str | None = Header(default=None)) -> None:
    if authorization != f"Bearer {settings.api_key}":
        raise HTTPException(status_code=401, detail="Invalid API key")


def enforce_limits(text: str) -> None:
    if len(text) > settings.max_input_chars:
        raise HTTPException(status_code=413, detail=f"Input exceeds {settings.max_input_chars} characters")


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok", provider=settings.provider, mode="local" if settings.provider == "mock" else "remote")


@app.post("/v1/chat", response_model=ModelResponse, dependencies=[Depends(require_api_key)])
async def chat(request: ChatInput) -> ModelResponse:
    for message in request.messages:
        enforce_limits(message.get("content", ""))
    return await get_provider().chat(request)


@app.post("/v1/classify", response_model=ModelResponse, dependencies=[Depends(require_api_key)])
async def classify(request: ClassifyInput) -> ModelResponse:
    enforce_limits(request.text)
    return await get_provider().classify(request)


@app.post("/v1/extract", response_model=ModelResponse, dependencies=[Depends(require_api_key)])
async def extract(request: ExtractInput) -> ModelResponse:
    enforce_limits(request.text)
    return await get_provider().extract(request)


@app.post("/v1/summarize", response_model=ModelResponse, dependencies=[Depends(require_api_key)])
async def summarize(request: TextInput) -> ModelResponse:
    enforce_limits(request.text)
    return await get_provider().summarize(request)
