from unittest.mock import AsyncMock, MagicMock

import pytest

from phoenixrpa.workflow.models import WorkflowStep
from phoenixrpa.workflow.runner import WorkflowRunner


@pytest.mark.asyncio
async def test_retry_uses_one_execution_log():
    dispatcher = MagicMock()

    dispatcher.dispatch = AsyncMock(
        side_effect=[
            RuntimeError("temporary failure"),
            None,
        ]
    )

    browser = MagicMock()

    execution_service = MagicMock()

    runner = WorkflowRunner(
        browser=browser,
        db=MagicMock(),
    )

    runner.dispatcher = dispatcher
    runner.execution_service = execution_service
    runner.run_id = 1

    step = WorkflowStep(
        action="click",
        selector="#userName",
        retries=1,
        timeout=30000,
        job_id=16,
        step_order=2,
    )

    await runner.run_step(
        step,
        log_execution=True,
    )

    # One logical step = one execution log.
    execution_service.start_step.assert_called_once()

    # The same log is marked successful after the retry succeeds.
    execution_service.finish_step.assert_called_once()

    # No final failure should be recorded.
    execution_service.fail_step.assert_not_called()

    # Dispatcher was actually attempted twice.
    assert dispatcher.dispatch.await_count == 2
