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
