from unittest.mock import AsyncMock, MagicMock

import pytest

from phoenixrpa.workflow.dispatcher import WorkflowDispatcher
from phoenixrpa.workflow.models import WorkflowStep
from phoenixrpa.workflow.variables import VariableResolver


@pytest.mark.asyncio
async def test_wait_text_resolves_workflow_variable():
    browser = MagicMock()
    browser.waits.text = AsyncMock()

    variables = VariableResolver()
    variables.set(
        "customer_name",
        "Rahul Kumar",
    )

    db = MagicMock()

    dispatcher = WorkflowDispatcher(
        browser=browser,
        variables=variables,
        db=db,
    )

    step = WorkflowStep(
        action="wait_text",
        value="{{customer_name}}",
    )

    result = await dispatcher.dispatch(step)

    assert result is None

    browser.waits.text.assert_awaited_once_with(
        "Rahul Kumar",
        timeout=step.timeout,
    )
