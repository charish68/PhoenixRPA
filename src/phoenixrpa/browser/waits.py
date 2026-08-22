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
    async def text(
        self,
        text: str,
        timeout: int = 30000,
    ):
        logger.info(
            f"Waiting for text '{text}'"
        )

        await self.page.get_by_text(
            text,
            exact=False,
        ).wait_for(
            state="visible",
            timeout=timeout,
        )


