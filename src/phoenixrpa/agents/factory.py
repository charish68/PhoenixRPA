from phoenixrpa.agents.mock_provider import MockLLMProvider
from phoenixrpa.agents.openai_compatible_provider import (
    OpenAICompatibleProvider,
)
from phoenixrpa.agents.provider import LLMProvider
from phoenixrpa.core.config import Settings


def create_llm_provider(
    settings: Settings,
) -> LLMProvider:

    provider = settings.llm_provider.lower()

    if provider == "mock":
        return MockLLMProvider(
            response="#emailInputChanged"
        )

    if provider in {"openai", "groq"}:

        if not settings.llm_api_key:
            raise ValueError(
                f"LLM_API_KEY is required "
                f"for the {provider} provider."
            )

        return OpenAICompatibleProvider(
            api_key=settings.llm_api_key,
            model=settings.llm_model,
            base_url=settings.llm_base_url,
            timeout=settings.llm_timeout,
        )

    raise ValueError(
        f"Unsupported LLM provider: "
        f"{settings.llm_provider}"
    )
