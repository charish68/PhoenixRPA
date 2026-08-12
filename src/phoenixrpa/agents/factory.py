from phoenixrpa.agents.mock_provider import MockLLMProvider
from phoenixrpa.agents.provider import LLMProvider
from phoenixrpa.core.config import Settings


def create_llm_provider(settings: Settings) -> LLMProvider:
    provider = settings.llm_provider.lower()

    if provider == "mock":
        return MockLLMProvider(
            response="#emailInputChanged"
        )

    raise ValueError(
        f"Unsupported LLM provider: {settings.llm_provider}"
    )
