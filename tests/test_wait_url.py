from unittest.mock import AsyncMock, MagicMock

import pytest

from phoenixrpa.workflow.dispatcher import WorkflowDispatcher
from phoenixrpa.workflow.models import WorkflowStep
from phoenixrpa.workflow.variables import VariableResolver


@pytest.mark.asyncio
async def test_wait_url_resolves_workflow_variable():
    browser = MagicMock()
    browser.waits.url = AsyncMock()

    variables = VariableResolver()
    variables.set(
        "dashboard_url",
        "https://example.com/dashboard",
    )

    db = MagicMock()

    dispatcher = WorkflowDispatcher(
        browser=browser,
        variables=variables,
        db=db,
    )

    step = WorkflowStep(
        action="wait_url",
        value="{{dashboard_url}}",
    )

    result = await dispatcher.dispatch(step)

    assert result is None

    browser.waits.url.assert_awaited_once_with(
        "https://example.com/dashboard",
        timeout=step.timeout,
    )
