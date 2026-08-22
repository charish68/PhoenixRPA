from unittest.mock import AsyncMock, MagicMock

import pytest

from phoenixrpa.workflow.dispatcher import WorkflowDispatcher
from phoenixrpa.workflow.models import WorkflowStep
from phoenixrpa.workflow.variables import VariableResolver


@pytest.mark.asyncio
async def test_click_resolves_variable_selector():
    browser = MagicMock()
    browser.actions.click = AsyncMock()

    variables = VariableResolver()
    variables.set(
        "login_button",
        "#loginButton",
    )

    dispatcher = WorkflowDispatcher(
        browser=browser,
        variables=variables,
        db=MagicMock(),
    )

    step = WorkflowStep(
        action="click",
        selector="{{login_button}}",
    )

    await dispatcher.dispatch(step)

    browser.actions.click.assert_awaited_once_with(
        "#loginButton",
        timeout=30000,
    )

    assert step.selector == "{{login_button}}"
