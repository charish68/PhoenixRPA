from unittest.mock import AsyncMock, MagicMock

import pytest

from phoenixrpa.workflow.models import WorkflowStep
from phoenixrpa.workflow.runner import WorkflowRunner


@pytest.mark.asyncio
async def test_wait_url_resolves_variable():
    browser = MagicMock()
    browser.waits.url = AsyncMock()

    runner = WorkflowRunner(
        browser=browser,
        variables={
            "expected_url": "https://example.com/dashboard",
        },
        db=MagicMock(),
    )

    step = WorkflowStep(
        action="wait_url",
        value="{{expected_url}}",
    )

    await runner.run_step(step)

    browser.waits.url.assert_awaited_once_with(
        "https://example.com/dashboard",
        timeout=30000,
    )
