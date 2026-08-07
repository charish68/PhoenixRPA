from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "PhoenixRPA"
    app_env: str = "development"
    debug: bool = True

    host: str = "127.0.0.1"
    port: int = 8000

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()