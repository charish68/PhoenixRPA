from phoenixrpa.core.config import Settings


def test_settings_load_llm_configuration(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgresql://test")
    monkeypatch.setenv(
        "PHOENIXRPA_EXTENSION_PATH",
        ".",
    )
    monkeypatch.setenv(
        "LLM_PROVIDER",
        "openai",
    )
    monkeypatch.setenv(
        "LLM_API_KEY",
        "test-key",
    )
    monkeypatch.setenv(
        "LLM_MODEL",
        "test-model",
    )
    monkeypatch.setenv(
        "LLM_BASE_URL",
        "https://example.com/v1",
    )
    monkeypatch.setenv(
        "LLM_TIMEOUT",
        "15",
    )

    settings = Settings()

    assert settings.llm_provider == "openai"
    assert settings.llm_api_key == "test-key"
    assert settings.llm_model == "test-model"
    assert settings.llm_base_url == "https://example.com/v1"
    assert settings.llm_timeout == 15.0
