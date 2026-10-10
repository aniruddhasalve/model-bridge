# Security

Never commit provider API keys or production project keys. Keep provider credentials server-side. Use HTTPS for deployed clients and APIs. Treat submitted text as potentially sensitive and define retention and redaction rules before logging.

The local API key is intentionally predictable for development only. Replace it before deployment. Production hosting should use hashed, revocable, project-scoped keys rather than one shared environment key.

Model output is untrusted data. Validate structured results before using them for authorization, database writes, user-visible claims, or code execution. Do not use an ML response as the sole security decision.
