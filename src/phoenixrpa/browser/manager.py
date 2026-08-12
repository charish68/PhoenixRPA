import asyncio
from pathlib import Path

from playwright.async_api import (
    Browser,
    BrowserContext,
    Page,
    Playwright,
    async_playwright,
)

from phoenixrpa.browser.actions import BrowserActions
from phoenixrpa.browser.extractor import BrowserExtractor
from phoenixrpa.browser.navigator import BrowserNavigator
from phoenixrpa.browser.screenshots import ScreenshotService
from phoenixrpa.browser.waits import BrowserWaits
from phoenixrpa.core.logger import logger
from phoenixrpa.healing.service import HealingService
from phoenixrpa.recorder.service import RecorderService
from phoenixrpa.core.config import settings
from phoenixrpa.agents.factory import create_llm_provider
from phoenixrpa.agents.healing_agent import AIHealingAgent


class BrowserManager:

    def __init__(self):

        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None

        self.actions: BrowserActions | None = None
        self.navigator: BrowserNavigator | None = None
        self.extractor: BrowserExtractor | None = None
        self.screenshots: ScreenshotService | None = None
        self.waits: BrowserWaits | None = None
        self.healer: HealingService | None = None

        # Recorder
        self.recorder = RecorderService()

    async def start(
        self,
        headless: bool = True,
    ) -> Page:
        """
        Start Playwright browser.

        When running with headless=False, the PhoenixRPA
        Chrome extension is loaded automatically.
        """

        # --------------------------------------------------
        # Prevent starting browser twice
        # --------------------------------------------------

        if self.page is not None:
            logger.info(
                "Browser already running"
            )
            return self.page

        logger.info(
            "Starting Playwright"
        )

        # --------------------------------------------------
        # Windows event loop information
        # --------------------------------------------------

        loop = asyncio.get_running_loop()

        logger.info(
            f"Running loop: {loop}"
        )

        logger.info(
            f"Loop class: {loop.__class__.__name__}"
        )

        logger.info(
            f"Loop module: {loop.__class__.__module__}"
        )

        # --------------------------------------------------
        # Start Playwright
        # --------------------------------------------------

        self.playwright = (
            await async_playwright().start()
        )

        # --------------------------------------------------
        # Find PhoenixRPA extension
        # --------------------------------------------------

        extension_path = settings.phoenixrpa_extension_path

        if extension_path:
            extension_path = str(
                Path(extension_path).resolve()
            )

        # --------------------------------------------------
        # Launch browser
        # --------------------------------------------------

        if headless:

            # Extensions cannot be used with
            # normal headless Chromium.
            #
            # Use regular Chromium for headless mode.

            logger.info(
                "Launching Chromium in headless mode"
            )

            self.browser = (
                await self.playwright.chromium.launch(
                    headless=True,
                )
            )

            self.context = (
                await self.browser.new_context()
            )

        else:

            # --------------------------------------------------
            # Extension mode
            # --------------------------------------------------

            if not extension_path:

                raise RuntimeError(
                    "PHOENIXRPA_EXTENSION_PATH is not set. "
                    "Set it to the folder containing "
                    "manifest.json, content.js and background.js."
                )

            extension_dir = Path(
                extension_path
            )

            manifest_file = (
                extension_dir / "manifest.json"
            )

            if not extension_dir.exists():

                raise RuntimeError(
                    f"PhoenixRPA extension directory "
                    f"does not exist: {extension_dir}"
                )

            if not manifest_file.exists():

                raise RuntimeError(
                    f"manifest.json not found in: "
                    f"{extension_dir}"
                )

            logger.info(
                f"Loading PhoenixRPA extension from: "
                f"{extension_dir}"
            )

            # --------------------------------------------------
            # Persistent Chromium context
            #
            # Required for loading unpacked extensions.
            # --------------------------------------------------

            user_data_dir = (
                Path.cwd()
                / ".phoenixrpa_browser_profile"
            )

            user_data_dir.mkdir(
                parents=True,
                exist_ok=True,
            )

            logger.info(
                f"Browser profile: {user_data_dir}"
            )

            self.context = (
                await self.playwright.chromium
                .launch_persistent_context(
                    user_data_dir=str(
                        user_data_dir
                    ),
                    headless=False,
                    args=[
                        f"--disable-extensions-except={extension_dir}",
                        f"--load-extension={extension_dir}",
                    ],
                )
            )

            # Persistent context owns the browser.
            self.browser = self.context.browser

        # --------------------------------------------------
        # Create page
        # --------------------------------------------------

        if self.context.pages:

            self.page = self.context.pages[0]

        else:

            self.page = (
                await self.context.new_page()
            )

        # --------------------------------------------------
        # Detect extension service worker
        # --------------------------------------------------

        if not headless:

            try:

                service_workers = (
                    self.context.service_workers
                )

                if service_workers:

                    logger.success(
                        "PhoenixRPA extension "
                        "service worker detected"
                    )

                else:

                    logger.warning(
                        "PhoenixRPA extension service "
                        "worker not detected yet"
                    )

            except Exception as e:

                logger.warning(
                    f"Could not inspect extension "
                    f"service worker: {e}"
                )

        # --------------------------------------------------
        # Healing service
        # --------------------------------------------------
        llm_provider = create_llm_provider(
            settings
        )

        ai_agent = AIHealingAgent(
            provider=llm_provider
        )

        self.healer = HealingService(
            self.page,
            ai_agent=ai_agent,
        )

        # --------------------------------------------------
        # Browser services
        # --------------------------------------------------

        self.actions = BrowserActions(
            self.page,
            self.healer,
            self.recorder,
        )

        self.navigator = BrowserNavigator(
            self.page,
            self.recorder,
        )

        self.extractor = BrowserExtractor(
            self.page,
        )

        self.screenshots = ScreenshotService(
            self.page,
        )

        self.waits = BrowserWaits(
            self.page,
        )

        logger.success(
            "Browser started successfully"
        )

        return self.page

    async def close(self) -> None:
        """
        Close browser resources.
        """

        logger.info(
            "Closing browser"
        )

        # --------------------------------------------------
        # Close context
        # --------------------------------------------------

        if self.context:

            try:

                await self.context.close()

            except Exception as e:

                logger.warning(
                    f"Error closing browser context: {e}"
                )

        # --------------------------------------------------
        # Close browser
        # --------------------------------------------------

        # With persistent context, closing the context
        # already closes Chromium.

        if self.browser:

            try:

                if self.browser.is_connected():

                    await self.browser.close()

            except Exception as e:

                logger.warning(
                    f"Error closing browser: {e}"
                )

        # --------------------------------------------------
        # Stop Playwright
        # --------------------------------------------------

        if self.playwright:

            try:

                await self.playwright.stop()

            except Exception as e:

                logger.warning(
                    f"Error stopping Playwright: {e}"
                )

        # --------------------------------------------------
        # Reset state
        # --------------------------------------------------

        self.page = None
        self.context = None
        self.browser = None
        self.playwright = None

        self.actions = None
        self.navigator = None
        self.extractor = None
        self.screenshots = None
        self.waits = None
        self.healer = None

        logger.info(
            "Browser closed"
        )