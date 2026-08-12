from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from phoenixrpa.browser.manager import BrowserManager
from phoenixrpa.agents.healing_agent import AIHealingAgent
from phoenixrpa.healing.service import HealingService


@pytest.mark.asyncio
async def test_browser_manager_wires_ai_healing_provider():

    fake_page = MagicMock()

    fake_context = MagicMock()
    fake_context.pages = [fake_page]

    fake_browser = MagicMock()

    fake_browser.new_context = AsyncMock(
        return_value=fake_context
    )

    fake_chromium = MagicMock()
    fake_chromium.launch = AsyncMock(
        return_value=fake_browser
    )

    fake_playwright = MagicMock()
    fake_playwright.chromium = fake_chromium

    fake_async_playwright = MagicMock()
    fake_async_playwright.start = AsyncMock(
        return_value=fake_playwright
    )

    manager = BrowserManager()

    with patch(
        "phoenixrpa.browser.manager.async_playwright",
        return_value=fake_async_playwright,
    ), patch(
        "phoenixrpa.browser.manager.create_llm_provider",
    ) as mock_factory:

        fake_provider = MagicMock()
        mock_factory.return_value = fake_provider

        await manager.start(headless=True)

    assert manager.page is fake_page

    mock_factory.assert_called_once()

    assert isinstance(
        manager.healer,
        HealingService,
    )

    assert isinstance(
        manager.healer.ai_agent,
        AIHealingAgent,
    )

    assert (
        manager.healer.ai_agent.provider
        is fake_provider
    )
