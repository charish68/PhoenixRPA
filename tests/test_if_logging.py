from unittest.mock import AsyncMock, MagicMock

import pytest

from phoenixrpa.workflow.models import WorkflowStep
from phoenixrpa.workflow.runner import WorkflowRunner


@pytest.mark.asyncio
async def test_if_step_stays_success_when_child_fails():
    dispatcher = MagicMock()

    dispatcher.dispatch = AsyncMock(
        side_effect=RuntimeError("child failed")
    )

    browser = MagicMock()
    execution_service = MagicMock()

    # The IF step itself is executed by the runner.
    runner = WorkflowRunner(
        browser=browser,
        db=MagicMock(),
    )

    runner.dispatcher = dispatcher
    runner.execution_service = execution_service
    runner.run_id = 100

    step = WorkflowStep(
        action="if",
        condition="success == success",
        retries=0,
        timeout=30000,
        job_id=16,
        step_order=4,
    )

    with pytest.raises(RuntimeError, match="child failed"):
        await runner.run_step(
            step,
            log_execution=True,
            branch_path="true",
        )

    # The IF itself must be recorded as successful.
    execution_service.finish_step.assert_called_once()

    # The IF must not be marked FAILED.
    execution_service.fail_step.assert_not_called()
