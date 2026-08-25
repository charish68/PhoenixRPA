from unittest.mock import AsyncMock, MagicMock

import pytest

from phoenixrpa.workflow.models import WorkflowStep
from phoenixrpa.workflow.runner import WorkflowRunner


@pytest.mark.asyncio
async def test_failed_step_captures_screenshot():
    dispatcher = MagicMock()

    dispatcher.dispatch = AsyncMock(
        side_effect=RuntimeError("element not found")
    )

    browser = MagicMock()
    browser.screenshots.capture_page = AsyncMock()

    execution_service = MagicMock()

    runner = WorkflowRunner(
        browser=browser,
        db=MagicMock(),
    )

    runner.dispatcher = dispatcher
    runner.execution_service = execution_service
    runner.run_id = 99

    step = WorkflowStep(
        action="click",
        selector="#missing",
        retries=0,
        timeout=30000,
        job_id=16,
        step_order=5,
    )

    with pytest.raises(RuntimeError, match="element not found"):
        await runner.run_step(
            step,
            log_execution=True,
        )

    browser.screenshots.capture_page.assert_awaited_once()

    screenshot_path = (
        browser.screenshots.capture_page.await_args.args[0]
    )

    assert "job_16_run_99_step_5_failure.png" in screenshot_path

    execution_service.fail_step.assert_called_once()

@pytest.mark.asyncio
async def test_failed_step_continues_when_screenshot_capture_fails():
    dispatcher = MagicMock()

    dispatcher.dispatch = AsyncMock(
        side_effect=RuntimeError("element not found")
    )

    browser = MagicMock()
    browser.screenshots.capture_page = AsyncMock(
        side_effect=RuntimeError("screenshot failed")
    )

    execution_service = MagicMock()

    runner = WorkflowRunner(
        browser=browser,
        db=MagicMock(),
    )

    runner.dispatcher = dispatcher
    runner.execution_service = execution_service
    runner.run_id = 99

    step = WorkflowStep(
        action="click",
        selector="#missing",
        retries=0,
        timeout=30000,
        job_id=16,
        step_order=5,
    )

    with pytest.raises(
        RuntimeError,
        match="element not found",
    ):
        await runner.run_step(
            step,
            log_execution=True,
        )

    browser.screenshots.capture_page.assert_awaited_once()

    execution_service.fail_step.assert_called_once()
