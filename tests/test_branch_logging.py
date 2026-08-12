from unittest.mock import AsyncMock, MagicMock

import pytest

from phoenixrpa.workflow.models import WorkflowStep
from phoenixrpa.workflow.runner import WorkflowRunner


@pytest.mark.asyncio
async def test_nested_step_records_branch_path():
    dispatcher = MagicMock()
    dispatcher.dispatch = AsyncMock(return_value=None)

    browser = MagicMock()
    execution_service = MagicMock()

    execution_log = MagicMock()

    execution_service.start_step.return_value = execution_log

    runner = WorkflowRunner(
        browser=browser,
        db=MagicMock(),
    )

    runner.dispatcher = dispatcher
    runner.execution_service = execution_service
    runner.run_id = 101

    step = WorkflowStep(
        action="click",
        selector="#userName",
        retries=0,
        timeout=30000,
        job_id=16,
        step_order=5,
    )

    await runner.run_step(
        step,
        log_execution=True,
        branch_path="true.true",
    )

    execution_service.start_step.assert_called_once_with(
        job_id=16,
        step_order=5,
        action="click",
        run_id=101,
        branch_path="true.true",
        original_selector="#userName",
    )

    execution_service.finish_step.assert_called_once_with(
        execution_log
    )
