from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    app_name: str = "PhoenixRPA"
    app_env: str = "development"
    debug: bool = True

    host: str = "127.0.0.1"
    port: int = 8000

    database_url: str

    phoenixrpa_extension_path: str

    # LLM configuration
    llm_provider: str = "mock"
    llm_api_key: str | None = None
    llm_model: str = "default"
    llm_base_url: str = "https://api.openai.com/v1"
    llm_timeout: float = 30.0

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
