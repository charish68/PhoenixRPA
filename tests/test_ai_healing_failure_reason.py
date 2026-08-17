import pytest
from unittest.mock import AsyncMock, MagicMock

from phoenixrpa.healing.service import HealingService


def make_page():
    page = MagicMock()

    failed_locator = MagicMock()
    failed_locator.count = AsyncMock(return_value=0)

    candidates = MagicMock()
    candidates.all = AsyncMock(return_value=[])

    body_locator = MagicMock()
    body_locator.inner_text = AsyncMock(return_value="<input>")

    def locator(selector):
        if selector == "#userEmail":
            return failed_locator

        if selector == "input, textarea, button, a, select":
            return candidates

        if selector == "body":
            return body_locator

        unknown = MagicMock()
        unknown.count = AsyncMock(return_value=0)
        return unknown

    page.locator.side_effect = locator

    return page


@pytest.mark.asyncio
async def test_ai_validation_failure_returns_failure_reason():
    page = make_page()

    invalid_locator = MagicMock()
    invalid_locator.count = AsyncMock(return_value=0)

    page.locator.side_effect = lambda selector: (
        invalid_locator
        if selector == "#invalidSelector"
        else (
            page.locator.side_effect.original(selector)
            if hasattr(page.locator.side_effect, "original")
            else MagicMock()
        )
    )


@pytest.mark.asyncio
async def test_no_ai_agent_returns_failure_reason():
    page = make_page()

    service = HealingService(page, ai_agent=None)

    result = await service.find_best_selector(
        "#userEmail",
        return_result=True,
    )

    assert result is not None
    assert result.status == "FAILED"
    assert result.method == "AI"
    assert result.failure_reason == "NO_AI_AGENT"


@pytest.mark.asyncio
async def test_ai_empty_response_returns_failure_reason():
    page = make_page()

    ai_agent = MagicMock()
    ai_agent.suggest_selector = AsyncMock(
        return_value=""
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
    assert result.status == "FAILED"
    assert result.method == "AI"
    assert result.failure_reason == "AI_NO_SELECTOR"

@pytest.mark.asyncio
async def test_ai_exception_returns_failure_reason():
    page = MagicMock()

    failed_locator = MagicMock()
    failed_locator.count = AsyncMock(return_value=0)

    candidates = MagicMock()
    candidates.all = AsyncMock(return_value=[])

    body_locator = MagicMock()
    body_locator.inner_text = AsyncMock(
        return_value="<input>"
    )

    def locator(selector):
        if selector == "#userEmail":
            return failed_locator

        if selector == "input, textarea, button, a, select":
            return candidates

        if selector == "body":
            return body_locator

        unknown = MagicMock()
        unknown.count = AsyncMock(return_value=0)
        return unknown

    page.locator.side_effect = locator

    ai_agent = MagicMock()
    ai_agent.suggest_selector = AsyncMock(
        side_effect=RuntimeError("LLM unavailable")
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
    assert result.status == "FAILED"
    assert result.method == "AI"
    assert result.failure_reason == "AI_EXCEPTION"
