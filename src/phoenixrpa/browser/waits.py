from playwright.async_api import Page

from phoenixrpa.core.logger import logger


class BrowserWaits:
    def __init__(self, page: Page):
        self.page = page

    async def element(
        self,
        selector: str,
        timeout: int = 30000,
    ):
        logger.info(f"Waiting for {selector}")

        await self.page.wait_for_selector(
            selector,
            timeout=timeout,
        )

    async def url(
        self,
        url: str,
        timeout: int = 30000,
    ):
        logger.info(f"Waiting for URL {url}")

        await self.page.wait_for_url(
            url,
            timeout=timeout,
        )