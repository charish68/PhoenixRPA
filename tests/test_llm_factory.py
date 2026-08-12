import pytest

from phoenixrpa.agents.factory import create_llm_provider
from phoenixrpa.agents.mock_provider import MockLLMProvider
from phoenixrpa.agents.openai_compatible_provider import (
    OpenAICompatibleProvider,
)
from phoenixrpa.core.config import Settings


def make_settings(
    provider: str,
    api_key: str | None = None,
) -> Settings:
    return Settings(
        database_url="postgresql://test",
        phoenixrpa_extension_path=".",
        llm_provider=provider,
        llm_api_key=api_key,
        llm_model="test-model",
        llm_base_url="https://example.com/v1",
        llm_timeout=10.0,
    )


def test_factory_creates_mock_provider():
    provider = create_llm_provider(
        make_settings("mock")
    )

    assert isinstance(
        provider,
        MockLLMProvider,
    )


@pytest.mark.parametrize(
    "provider_name",
    ["openai", "groq"],
)
def test_factory_creates_openai_compatible_provider(
    provider_name,
):
    provider = create_llm_provider(
        make_settings(
            provider_name,
            api_key="test-key",
        )
    )

    assert isinstance(
        provider,
        OpenAICompatibleProvider,
    )

    assert provider.api_key == "test-key"
    assert provider.model == "test-model"
    assert provider.base_url == "https://example.com/v1"
    assert provider.timeout == 10.0


@pytest.mark.parametrize(
    "provider_name",
    ["openai", "groq"],
)
def test_factory_rejects_provider_without_api_key(
    provider_name,
):
    with pytest.raises(
        ValueError,
        match="LLM_API_KEY is required",
    ):
        create_llm_provider(
            make_settings(provider_name)
        )


@pytest.mark.parametrize(
    "provider_name",
    [
        "unknown",
        "invalid",
    ],
)
def test_factory_rejects_unsupported_provider(
    provider_name,
):
    with pytest.raises(ValueError):
        create_llm_provider(
            make_settings(provider_name)
        )
