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
