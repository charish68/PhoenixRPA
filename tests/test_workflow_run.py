from unittest.mock import AsyncMock, MagicMock

import pytest

from phoenixrpa.workflow.models import WorkflowStep
from phoenixrpa.workflow.runner import WorkflowRunner


@pytest.mark.asyncio
async def test_runner_executes_workflow_steps_in_order():
    runner = WorkflowRunner(
        browser=MagicMock(),
        db=MagicMock(),
    )

    runner.run_step = AsyncMock()

    step1 = WorkflowStep(
        action="click",
        selector="#userName",
        step_order=1,
    )

    step2 = WorkflowStep(
        action="click",
        selector="#userEmail",
        step_order=2,
    )

    workflow = MagicMock()
    workflow.steps = [step1, step2]

    await runner.run(workflow)

    assert runner.run_step.await_count == 2

    calls = runner.run_step.await_args_list

    assert calls[0].args[0] is step1
    assert calls[1].args[0] is step2

@pytest.mark.asyncio
async def test_runner_stops_workflow_after_step_failure():
    runner = WorkflowRunner(
        browser=MagicMock(),
        db=MagicMock(),
    )

    step1 = WorkflowStep(
        action="click",
        selector="#first",
        step_order=1,
    )

    step2 = WorkflowStep(
        action="click",
        selector="#second",
        step_order=2,
    )

    workflow = MagicMock()
    workflow.steps = [step1, step2]

    runner.run_step = AsyncMock(
        side_effect=RuntimeError("first step failed")
    )

    with pytest.raises(
        RuntimeError,
        match="first step failed",
    ):
        await runner.run(workflow)

    assert runner.run_step.await_count == 1

    runner.run_step.assert_awaited_once_with(
        step1,
        log_execution=True,
    )

@pytest.mark.asyncio
async def test_runner_enables_execution_logging_for_all_workflow_steps():
    runner = WorkflowRunner(
        browser=MagicMock(),
        db=MagicMock(),
    )

    runner.run_step = AsyncMock()

    steps = [
        WorkflowStep(
            action="click",
            selector="#first",
            step_order=1,
        ),
        WorkflowStep(
            action="click",
            selector="#second",
            step_order=2,
        ),
    ]

    workflow = MagicMock()
    workflow.steps = steps

    await runner.run(workflow)

    assert runner.run_step.await_count == 2

    for index, step in enumerate(steps):
        call = runner.run_step.await_args_list[index]

        assert call.args[0] is step
        assert call.kwargs["log_execution"] is True
