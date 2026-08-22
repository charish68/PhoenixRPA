from unittest.mock import AsyncMock, MagicMock

import pytest

from phoenixrpa.workflow.models import WorkflowStep
from phoenixrpa.workflow.runner import WorkflowRunner


@pytest.mark.asyncio
async def test_goto_resolves_variable():
    browser = MagicMock()
    browser.navigator.goto = AsyncMock()

    runner = WorkflowRunner(
        browser=browser,
        variables={
            "target_url": "https://example.com/dashboard",
        },
        db=MagicMock(),
    )

    step = WorkflowStep(
        action="goto",
        value="{{target_url}}",
    )

    await runner.run_step(step)

    browser.navigator.goto.assert_awaited_once_with(
        "https://example.com/dashboard",
        timeout=30000,
    )
