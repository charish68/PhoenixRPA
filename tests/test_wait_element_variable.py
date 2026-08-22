from unittest.mock import AsyncMock, MagicMock

import pytest

from phoenixrpa.workflow.dispatcher import WorkflowDispatcher
from phoenixrpa.workflow.models import WorkflowStep
from phoenixrpa.workflow.variables import VariableResolver


@pytest.mark.asyncio
async def test_wait_element_resolves_variable_selector():
    browser = MagicMock()

    browser.waits.element = AsyncMock()

    variables = VariableResolver()
    variables.set(
        "login_button_selector",
        "#loginButton",
    )

    db = MagicMock()

    dispatcher = WorkflowDispatcher(
        browser=browser,
        variables=variables,
        db=db,
    )

    step = WorkflowStep(
        action="wait_element",
        selector="{{login_button_selector}}",
    )

    await dispatcher.dispatch(step)

    browser.waits.element.assert_awaited_once_with(
        "#loginButton",
        timeout=30000,
    )
