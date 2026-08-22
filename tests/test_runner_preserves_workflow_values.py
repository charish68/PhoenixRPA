from unittest.mock import AsyncMock, MagicMock

import pytest

from phoenixrpa.workflow.models import WorkflowStep
from phoenixrpa.workflow.runner import WorkflowRunner


@pytest.mark.asyncio
async def test_run_step_restores_original_variable_values():
    browser = MagicMock()
    db = MagicMock()

    runner = WorkflowRunner(
        browser=browser,
        variables={
            "button": "#loginButton",
            "message": "Hello",
            "file_path": "screenshots/test.png",
        },
        db=db,
    )

    runner.dispatcher.dispatch = AsyncMock(
        return_value=None
    )

    step = WorkflowStep(
        action="fill",
        selector="{{button}}",
        value="{{message}}",
        path="{{file_path}}",
    )

    await runner.run_step(step)

    assert step.selector == "{{button}}"
    assert step.value == "{{message}}"
    assert step.path == "{{file_path}}"
