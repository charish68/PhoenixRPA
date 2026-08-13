import pytest
from unittest.mock import AsyncMock, MagicMock

from phoenixrpa.agents.factory import create_llm_provider
from phoenixrpa.agents.healing_agent import AIHealingAgent
from phoenixrpa.core.config import Settings
from phoenixrpa.healing.service import HealingService


@pytest.mark.asyncio
@pytest.mark.integration
async def test_groq_ai_healing_integration():

    page = MagicMock()

    original_locator = MagicMock()
    original_locator.count = AsyncMock(return_value=0)

    candidates_locator = MagicMock()
    candidates_locator.all = AsyncMock(return_value=[])

    body_locator = MagicMock()
    body_locator.inner_text = AsyncMock(
        return_value=(
            '<input id="emailInputChanged" '
            'type="email">'
        )
    )

    ai_locator = MagicMock()
    ai_locator.count = AsyncMock(return_value=1)

    def locator(selector):
        if selector == "#userEmail":
            return original_locator

        if selector == "input, textarea, button, a, select":
            return candidates_locator

        if selector == "body":
            return body_locator

        if selector in (
            "#emailInputChanged",
            "input#emailInputChanged",
        ):
            return ai_locator

        unknown_locator = MagicMock()
        unknown_locator.count = AsyncMock(return_value=0)
        return unknown_locator

    page.locator.side_effect = locator

    settings = Settings(
        database_url="postgresql://test",
        phoenixrpa_extension_path=".",
        llm_provider="groq",
        llm_api_key=None,
        llm_model="llama-3.1-8b-instant",
        llm_base_url="https://api.groq.com/openai/v1",
        llm_timeout=30.0,
    )

    # Read the real key from the normal application settings.
    from phoenixrpa.core.config import get_settings

    settings = get_settings()

    if settings.llm_provider.lower() != "groq":
        pytest.skip("LLM_PROVIDER is not configured as groq")

    if not settings.llm_api_key:
        pytest.skip("LLM_API_KEY is not configured")

    provider = create_llm_provider(settings)
    agent = AIHealingAgent(provider=provider)

    service = HealingService(
        page,
        ai_agent=agent,
    )

    result = await service.find_best_selector(
        "#userEmail"
    )

    assert result == "#emailInputChanged"
