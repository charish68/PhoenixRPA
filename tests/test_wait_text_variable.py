from unittest.mock import AsyncMock, MagicMock

import pytest

from phoenixrpa.workflow.models import WorkflowStep
from phoenixrpa.workflow.runner import WorkflowRunner


@pytest.mark.asyncio
async def test_wait_text_resolves_variable():
    browser = MagicMock()
    browser.waits.text = AsyncMock()

    runner = WorkflowRunner(
        browser=browser,
        variables={
            "expected_text": "Welcome",
        },
        db=MagicMock(),
    )

    step = WorkflowStep(
        action="wait_text",
        value="{{expected_text}}",
    )

    await runner.run_step(step)

    browser.waits.text.assert_awaited_once_with(
        "Welcome",
        timeout=30000,
    )
