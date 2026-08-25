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

@pytest.mark.asyncio
async def test_run_step_retries_with_resolved_values():

    browser = MagicMock()
    db = MagicMock()

    runner = WorkflowRunner(
        browser=browser,
        variables={
            "button": "#loginButton",
            "message": "Hello",
        },
        db=db,
    )

    step = WorkflowStep(
        action="fill",
        selector="{{button}}",
        value="{{message}}",
        retries=1,
    )

    captured_values = []

    async def dispatch_side_effect(
        dispatched_step,
        **kwargs,
    ):
        captured_values.append(
            (
                dispatched_step.selector,
                dispatched_step.value,
            )
        )

        if len(captured_values) == 1:
            raise RuntimeError("temporary failure")

        return None

    runner.dispatcher.dispatch = AsyncMock(
        side_effect=dispatch_side_effect
    )

    await runner.run_step(step)

    assert runner.dispatcher.dispatch.await_count == 2

    assert captured_values == [
        ("#loginButton", "Hello"),
        ("#loginButton", "Hello"),
    ]

    assert step.selector == "{{button}}"
    assert step.value == "{{message}}"


@pytest.mark.asyncio
async def test_run_step_restores_original_values_after_retries_fail():

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

    step = WorkflowStep(
        action="fill",
        selector="{{button}}",
        value="{{message}}",
        path="{{file_path}}",
        retries=1,
    )

    runner.dispatcher.dispatch = AsyncMock(
        side_effect=RuntimeError("persistent failure")
    )

    with pytest.raises(
        RuntimeError,
        match="persistent failure",
    ):
        await runner.run_step(step)

    assert runner.dispatcher.dispatch.await_count == 2

    assert step.selector == "{{button}}"
    assert step.value == "{{message}}"
    assert step.path == "{{file_path}}"
