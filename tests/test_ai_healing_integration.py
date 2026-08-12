import pytest
from unittest.mock import AsyncMock, MagicMock

from phoenixrpa.agents.healing_agent import AIHealingAgent
from phoenixrpa.healing.service import HealingService


@pytest.mark.asyncio
async def test_ai_fallback_heals_selector():

    page = MagicMock()

    # Original selector does not exist.
    original_locator = MagicMock()
    original_locator.count = AsyncMock(return_value=0)

    # No deterministic candidates.
    candidates_locator = MagicMock()
    candidates_locator.all = AsyncMock(return_value=[])

    # Body locator used by AI healing.
    body_locator = MagicMock()
    body_locator.inner_text = AsyncMock(
        return_value=(
            '<input id="emailInputChanged" '
            'type="email">'
        )
    )

    # AI-generated selector exists exactly once.
    ai_locator = MagicMock()
    ai_locator.count = AsyncMock(return_value=1)

    def locator(selector):

        if selector == "#userEmail":
            return original_locator

        if selector == "input, textarea, button, a, select":
            return candidates_locator

        if selector == "body":
            return body_locator

        if selector == "#emailInputChanged":
            return ai_locator

        return MagicMock()

    page.locator.side_effect = locator

    provider = MagicMock()
    provider.generate = AsyncMock(
        return_value="#emailInputChanged"
    )

    agent = AIHealingAgent(
        provider=provider,
    )

    service = HealingService(
        page,
        ai_agent=agent,
    )

    result = await service.find_best_selector(
        "#userEmail"
    )

    assert result == "#emailInputChanged"

    provider.generate.assert_awaited_once()
