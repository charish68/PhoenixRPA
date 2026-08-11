from playwright.async_api import Page

from phoenixrpa.core.logger import logger


class ScreenshotService:
    def __init__(self, page: Page):
        self._page = page

    async def capture_page(self, path: str):
        logger.info(f"Saving page screenshot: {path}")

        await self._page.screenshot(path=path)

        logger.info("Page screenshot saved")

    async def capture_element(
        self,
        selector: str,
        path: str,
    ):
        logger.info(f"Saving element screenshot: {selector}")

        await self._page.locator(selector).screenshot(path=path)

        logger.info("Element screenshot saved")