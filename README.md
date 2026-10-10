# ModelBridge

A provider-neutral ML gateway for projects that need chat, classification, extraction, summarization, or other model operations through one backend contract.

ModelBridge is designed to be used by another project's backend or frontend. The backend service keeps provider credentials on the server, applies input limits, and exposes a stable API. A deterministic mock provider makes local development and demos work without a model account.

## Start locally in mock mode

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
PYTHONPATH=backend uvicorn app.main:app --reload --port 8000
```

Open the API docs at `http://127.0.0.1:8000/docs`.

The default API key is only for local development:

```text
local-development-key
```

## Endpoints

| Method | Endpoint | Purpose |
| --- | --- | --- |
| GET | `/health` | Service status |
| POST | `/v1/chat` | Chat completion |
| POST | `/v1/classify` | Classify text into supplied labels |
| POST | `/v1/extract` | Extract requested fields |
| POST | `/v1/summarize` | Summarize text |

Example:

```bash
curl -X POST http://127.0.0.1:8000/v1/classify \
  -H 'Authorization: Bearer local-development-key' \
  -H 'Content-Type: application/json' \
  -d '{"text":"The checkout button is broken","labels":["bug","feature","question"]}'
```

## Use from another project

Python:

```python
from clients.python_client import ModelBridgeClient

client = ModelBridgeClient("https://your-modelbridge-host", "project-api-key")
result = client.summarize("Text from your application")
```

Browser JavaScript:

```javascript
import { ModelBridge } from "./model-bridge.js";
const ml = new ModelBridge({ baseUrl: "/api/ml", apiKey: "browser-safe-project-key" });
const result = await ml.classify("A user cannot sign in", ["bug", "support", "feedback"]);
```

Do not put a provider secret in frontend code. For a public browser application, proxy requests through your own backend or issue a tightly scoped project key with quotas.

## Use a real provider

Set environment variables on the server:

```bash
export MODEL_BRIDGE_PROVIDER=openai-compatible
export MODEL_BRIDGE_PROVIDER_BASE_URL=https://api.openai.com/v1
export MODEL_BRIDGE_PROVIDER_API_KEY=replace-me
export MODEL_BRIDGE_PROVIDER_MODEL=your-model
export MODEL_BRIDGE_API_KEY=replace-with-a-project-key
```

The adapter uses the common `/chat/completions` contract. Keep the provider key server-side and rotate it through your secret manager.

## Architecture

```text
Your frontend or backend
          |
          v
ModelBridge API key + stable request contract
          |
          v
Provider adapter: mock or OpenAI-compatible
          |
          v
Selected model provider
```

## Production work before public hosting

Add a database-backed project and API-key model, hashed key storage, key rotation and revocation, rate limits, quotas, request size limits, provider retry policy, structured output validation, request redaction, audit events, usage metering, monitoring, and a privacy policy. The local mock service is a safe development baseline, not a public multi-tenant service.

## License

MIT. See [LICENSE](LICENSE).
