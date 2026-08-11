from unittest.mock import AsyncMock, MagicMock

import pytest

from phoenixrpa.workflow.models import WorkflowStep
from phoenixrpa.workflow.runner import WorkflowRunner


@pytest.mark.asyncio
async def test_runner_fails_after_retries_exhausted():
    dispatcher = MagicMock()

    dispatcher.dispatch = AsyncMock(
        side_effect=RuntimeError("persistent failure")
    )

    browser = MagicMock()

    runner = WorkflowRunner(
        browser=browser,
        db=MagicMock(),
    )

    runner.dispatcher = dispatcher

    step = WorkflowStep(
        action="click",
        selector="#userName",
        retries=1,
        timeout=30000,
    )

    with pytest.raises(RuntimeError, match="persistent failure"):
        await runner.run_step(
            step,
            log_execution=False,
        )

    assert dispatcher.dispatch.await_count == 2
