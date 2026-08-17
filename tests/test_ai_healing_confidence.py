import pytest
from unittest.mock import AsyncMock, MagicMock

from phoenixrpa.healing.service import HealingService


@pytest.mark.asyncio
async def test_ai_healing_returns_validation_confidence():
    page = MagicMock()

    failed_locator = MagicMock()
    failed_locator.count = AsyncMock(return_value=0)

    candidates = MagicMock()
    candidates.all = AsyncMock(return_value=[])

    healed_locator = MagicMock()
    healed_locator.count = AsyncMock(return_value=1)

    body_locator = MagicMock()
    body_locator.inner_text = AsyncMock(
        return_value='<input id="emailInputChanged" type="email">'
    )

    def locator(selector):
        if selector == "#userEmail":
            return failed_locator

        if selector == "input, textarea, button, a, select":
            return candidates

        if selector == "#emailInputChanged":
            return healed_locator

        if selector == "body":
            return body_locator

        unknown = MagicMock()
        unknown.count = AsyncMock(return_value=0)
        return unknown

    page.locator.side_effect = locator

    ai_agent = MagicMock()
    ai_agent.suggest_selector = AsyncMock(
        return_value="#emailInputChanged"
    )

    service = HealingService(
        page,
        ai_agent=ai_agent,
    )

    result = await service.find_best_selector(
        "#userEmail",
        return_result=True,
    )

    assert result is not None
    assert result.method == "AI"
    assert result.healed_selector == "#emailInputChanged"
    assert result.confidence == pytest.approx(1.0)
