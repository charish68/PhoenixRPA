from unittest.mock import AsyncMock, MagicMock

import pytest

from phoenixrpa.workflow.dispatcher import WorkflowDispatcher
from phoenixrpa.workflow.models import WorkflowStep
from phoenixrpa.workflow.variables import VariableResolver


@pytest.mark.asyncio
async def test_fill_resolves_variable_selector_and_value():
    browser = MagicMock()
    browser.actions.fill = AsyncMock()

    variables = VariableResolver()
    variables.set(
        "email_selector",
        "#userEmail",
    )
    variables.set(
        "email",
        "rahul@example.com",
    )

    dispatcher = WorkflowDispatcher(
        browser=browser,
        variables=variables,
        db=MagicMock(),
    )

    step = WorkflowStep(
        action="fill",
        selector="{{email_selector}}",
        value="{{email}}",
    )

    await dispatcher.dispatch(step)

    browser.actions.fill.assert_awaited_once_with(
        "#userEmail",
        "rahul@example.com",
        timeout=30000,
    )

    assert step.selector == "{{email_selector}}"
