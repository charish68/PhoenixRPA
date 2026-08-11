from playwright.async_api import Page

from phoenixrpa.core.logger import logger


class BrowserExtractor:
    def __init__(self, page: Page):
        self.page = page

    async def text(
        self,
        selector: str,
    ) -> str:
        logger.info(f"Extracting text from {selector}")

        return await self.page.locator(selector).inner_text()

    async def html(
        self,
    ) -> str:
        logger.info("Extracting HTML")

        return await self.page.content()

    async def attribute(
        self,
        selector: str,
        attribute: str,
    ) -> str | None:
        logger.info(
            f"Extracting attribute '{attribute}' from {selector}"
        )

        return await self.page.locator(selector).get_attribute(
            attribute
        )