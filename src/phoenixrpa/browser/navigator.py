from playwright.async_api import Page

from phoenixrpa.core.logger import logger
from phoenixrpa.recorder.service import RecorderService


class BrowserNavigator:
    def __init__(
        self,
        page: Page,
        recorder: RecorderService,
    ):
        self.page = page
        self.recorder = recorder

    async def goto(
        self,
        url: str,
        timeout: int = 30000,
    ):
        logger.info(f"Navigating to {url}")

        # Record navigation
        self.recorder.record(
            action="goto",
            value=url,
        )

        await self.page.goto(
            url,
            wait_until="networkidle",
            timeout=timeout,
        )

        logger.info("Navigation completed")