from unittest.mock import AsyncMock, MagicMock

import pytest

from phoenixrpa.healing.service import HealingService


@pytest.mark.asyncio
async def test_healing_finds_matching_selector():
    page = MagicMock()

    original = MagicMock()
    original.count = AsyncMock(return_value=0)

    page.locator.side_effect = [
        original,
        MagicMock(),
    ]

    candidate = MagicMock()
    candidate.get_attribute = AsyncMock(
        side_effect=lambda name: {
            "id": "userName",
            "name": None,
            "data-testid": None,
            "aria-label": None,
            "placeholder": None,
        }.get(name)
    )
    candidate.evaluate = AsyncMock(
        return_value="input"
    )

    candidates_locator = MagicMock()
    candidates_locator.all = AsyncMock(
        return_value=[candidate]
    )

    page.locator.side_effect = [
        original,
        candidates_locator,
        MagicMock(count=AsyncMock(return_value=1)),
    ]

    service = HealingService(page)

    result = await service.find_best_selector(
        "#userNam"
    )

    assert result == "#userName"

@pytest.mark.asyncio
async def test_ai_healing_timeout_returns_none(monkeypatch):

    page = MagicMock()

    original = MagicMock()
    original.count = AsyncMock(return_value=0)

    candidates_locator = MagicMock()
    candidates_locator.all = AsyncMock(return_value=[])

    body_locator = MagicMock()
    body_locator.inner_text = AsyncMock(
        return_value="<input id='emailInputChanged'>"
    )

    page.locator.side_effect = [
        original,
        candidates_locator,
        body_locator,
    ]

    ai_agent = MagicMock()
    ai_agent.suggest_selector = AsyncMock(
        return_value="#emailInputChanged"
    )

    async def timeout_wait_for(awaitable, timeout):
        awaitable.close()
        raise TimeoutError()

    monkeypatch.setattr(
        "phoenixrpa.healing.service.asyncio.wait_for",
        timeout_wait_for,
    )

    service = HealingService(
        page,
        ai_agent=ai_agent,
    )

    result = await service.find_best_selector(
        "#userEmail"
    )

    assert result is None
    ai_agent.suggest_selector.assert_not_awaited()
