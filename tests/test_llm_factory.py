import pytest

from phoenixrpa.agents.factory import create_llm_provider
from phoenixrpa.agents.mock_provider import MockLLMProvider
from phoenixrpa.core.config import Settings


def make_settings(provider: str) -> Settings:
    return Settings(
        database_url="postgresql://test",
        phoenixrpa_extension_path=".",
        llm_provider=provider,
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
    [
        "unknown",
        "openai",
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
