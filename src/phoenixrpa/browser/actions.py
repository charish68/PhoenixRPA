from playwright.async_api import Page

from phoenixrpa.core.logger import logger
from phoenixrpa.healing.service import HealingService
from phoenixrpa.recorder.service import RecorderService


class BrowserActions:
    def __init__(
        self,
        page: Page,
        healer: HealingService,
        recorder: RecorderService,
    ):
        self.page = page
        self.healer = healer
        self.recorder = recorder

    async def click(
        self,
        selector: str,
        timeout: int = 30000,
    ):
        logger.info(f"Clicking: {selector}")

        self.recorder.record(
            action="click",
            selector=selector,
        )

        await self.page.locator(selector).click(
            timeout=timeout,
        )

    async def fill(
        self,
        selector: str,
        value: str,
        timeout: int = 30000,
    ):
        logger.info(f"Filling: {selector}")

        self.recorder.record(
            action="fill",
            selector=selector,
            value=value,
        )

        await self.page.locator(selector).fill(
            value,
            timeout=timeout,
        )

    async def press(
        self,
        selector: str,
        key: str,
        timeout: int = 30000,
    ):
        logger.info(f"Pressing '{key}' on {selector}")

        self.recorder.record(
            action="press",
            selector=selector,
            value=key,
        )

        await self.page.locator(selector).press(
            key,
            timeout=timeout,
        )

    async def hover(
        self,
        selector: str,
        timeout: int = 30000,
    ):
        logger.info(f"Hovering: {selector}")

        self.recorder.record(
            action="hover",
            selector=selector,
        )

        await self.page.locator(selector).hover(
            timeout=timeout,
        )