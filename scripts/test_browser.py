import asyncio

from phoenixrpa.browser.manager import BrowserManager
from phoenixrpa.engine.executor import ActionExecutor


async def main():
    browser = BrowserManager()

    executor = ActionExecutor()

    await browser.start(headless=False)

    await browser.navigator.goto("https://example.com")

    print(await browser.extractor.title())

    await executor.execute(
        "Screenshot",
        browser.screenshots.page,
        "example.png",
    )

    await browser.close()


if __name__ == "__main__":
    asyncio.run(main())