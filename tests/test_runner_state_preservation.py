from unittest.mock import AsyncMock, Mock

import pytest

from phoenixrpa.workflow.models import WorkflowStep
from phoenixrpa.workflow.runner import WorkflowRunner


@pytest.mark.asyncio
async def test_runner_restores_original_step_values_after_success():
    browser = Mock()
    db = Mock()

    runner = WorkflowRunner(
        browser=browser,
        variables={
            "selector": "#resolved",
            "value": "resolved-value",
            "path": "resolved.png",
        },
        db=db,
    )

    dispatch = AsyncMock()
    runner.dispatcher.dispatch = dispatch

    step = WorkflowStep(
        action="click",
        selector="{{selector}}",
        value="{{value}}",
        path="{{path}}",
    )

    await runner.run_step(step)

    assert step.selector == "{{selector}}"
    assert step.value == "{{value}}"
    assert step.path == "{{path}}"

@pytest.mark.asyncio
async def test_runner_restores_original_step_values_after_failure():
    browser = Mock()
    db = Mock()

    runner = WorkflowRunner(
        browser=browser,
        variables={
            "selector": "#resolved",
            "value": "resolved-value",
            "path": "resolved.png",
        },
        db=db,
    )

    dispatch = AsyncMock(
        side_effect=RuntimeError("Dispatch failed")
    )
    runner.dispatcher.dispatch = dispatch

    step = WorkflowStep(
        action="click",
        selector="{{selector}}",
        value="{{value}}",
        path="{{path}}",
    )

    with pytest.raises(
        RuntimeError,
        match="Dispatch failed",
    ):
        await runner.run_step(step)

    assert step.selector == "{{selector}}"
    assert step.value == "{{value}}"
    assert step.path == "{{path}}"
