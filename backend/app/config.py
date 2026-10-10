from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    api_key: str = "local-development-key"
    provider: str = "mock"
    provider_base_url: str = ""
    provider_api_key: str = ""
    provider_model: str = ""
    cors_origins: str = "http://127.0.0.1:8000,http://localhost:8000"
    max_input_chars: int = 12000
    model_config = SettingsConfigDict(env_prefix="MODEL_BRIDGE_", env_file=".env", extra="ignore")

    @property
    def allowed_origins(self) -> list[str]:
        return [value.strip() for value in self.cors_origins.split(",") if value.strip()]


settings = Settings()
