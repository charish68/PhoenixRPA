import asyncio

from phoenixrpa.browser.manager import BrowserManager
from phoenixrpa.workflow.models import Workflow
from phoenixrpa.workflow.runner import WorkflowRunner


workflow = Workflow(
    steps=[
        {
            "action": "goto",
            "value": "https://example.com",
        },
        {
            "action": "screenshot",
            "path": "workflow.png",
        },
    ]
)


async def main():

    browser = BrowserManager()

    await browser.start(headless=False)

    runner = WorkflowRunner(browser)

    await runner.run(workflow)

    await browser.close()


asyncio.run(main())