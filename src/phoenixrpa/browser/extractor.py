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
    async def table(
        self,
        selector: str,
    ) -> list[list[str]]:
        logger.info(
            f"Extracting table from {selector}"
        )

        rows = await self.page.locator(
            f"{selector} tr"
        ).all()

        table_data = []

        for row in rows:
            cells = await row.locator(
                "th, td"
            ).all_inner_texts()

            if cells:
                table_data.append(cells)

        return table_data


