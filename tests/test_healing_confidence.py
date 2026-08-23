import pytest
from unittest.mock import AsyncMock, MagicMock

from phoenixrpa.healing.service import HealingService


@pytest.mark.asyncio
async def test_deterministic_healing_returns_confidence():
    page = MagicMock()

    failed_locator = MagicMock()
    failed_locator.count = AsyncMock(return_value=0)

    element = MagicMock()
    element.get_attribute = AsyncMock(
        side_effect=lambda name: {
            "id": "userEmailChanged",
            "name": None,
            "data-testid": None,
            "aria-label": None,
            "placeholder": None,
        }.get(name)
    )
    element.evaluate = AsyncMock(
        return_value="input"
    )

    candidates = MagicMock()
    candidates.all = AsyncMock(
        return_value=[element]
    )

    healed_locator = MagicMock()
    healed_locator.count = AsyncMock(return_value=1)

    def locator(selector):
        if selector == "#userEmail":
            return failed_locator

        if selector == "input, textarea, button, a, select":
            return candidates

        if selector == "#userEmailChanged":
            return healed_locator

        unknown = MagicMock()
        unknown.count = AsyncMock(return_value=0)
        return unknown

    page.locator.side_effect = locator

    service = HealingService(page)

    result = await service.find_best_selector(
        "#userEmail",
        return_result=True,
    )

    assert result is not None
    assert result.method == "DETERMINISTIC"
    assert result.healed_selector == "#userEmailChanged"
    assert result.confidence == pytest.approx(
        15 / 21
    )



@pytest.mark.asyncio
async def test_deterministic_healing_skips_hidden_elements():
    page = MagicMock()

    failed_locator = MagicMock()
    failed_locator.count = AsyncMock(return_value=0)

    hidden_element = MagicMock()
    hidden_element.is_visible = AsyncMock(return_value=False)
    hidden_element.get_attribute = AsyncMock(
        side_effect=lambda name: {
            "id": "userEmailHidden",
            "name": None,
            "data-testid": None,
            "aria-label": None,
            "placeholder": None,
        }.get(name)
    )
    hidden_element.evaluate = AsyncMock(
        return_value="input"
    )

    visible_element = MagicMock()
    visible_element.is_visible = AsyncMock(return_value=True)
    visible_element.get_attribute = AsyncMock(
        side_effect=lambda name: {
            "id": "email",
            "name": None,
            "data-testid": None,
            "aria-label": None,
            "placeholder": None,
        }.get(name)
    )
    visible_element.evaluate = AsyncMock(
        return_value="input"
    )

    candidates = MagicMock()
    candidates.all = AsyncMock(
        return_value=[
            hidden_element,
            visible_element,
        ]
    )

    hidden_locator = MagicMock()
    hidden_locator.count = AsyncMock(return_value=1)

    visible_locator = MagicMock()
    visible_locator.count = AsyncMock(return_value=1)

    def locator(selector):
        if selector == "#userEmail":
            return failed_locator

        if selector == "input, textarea, button, a, select":
            return candidates

        if selector == "#userEmailHidden":
            return hidden_locator

        if selector == "#email":
            return visible_locator

        unknown = MagicMock()
        unknown.count = AsyncMock(return_value=0)
        return unknown

    page.locator.side_effect = locator

    service = HealingService(page)

    result = await service.find_best_selector(
        "#userEmail",
        return_result=True,
    )

    assert result is not None
    assert result.healed_selector == "#email"
