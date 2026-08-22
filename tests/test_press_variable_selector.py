from unittest.mock import AsyncMock, MagicMock

import pytest

from phoenixrpa.workflow.dispatcher import WorkflowDispatcher
from phoenixrpa.workflow.models import WorkflowStep
from phoenixrpa.workflow.variables import VariableResolver


@pytest.mark.asyncio
async def test_press_resolves_variable_selector_and_value():
    browser = MagicMock()
    browser.actions.press = AsyncMock()

    variables = VariableResolver()
    variables.set(
        "search_selector",
        "#searchInput",
    )
    variables.set(
        "key",
        "Enter",
    )

    dispatcher = WorkflowDispatcher(
        browser=browser,
        variables=variables,
        db=MagicMock(),
    )

    step = WorkflowStep(
        action="press",
        selector="{{search_selector}}",
        value="{{key}}",
    )

    await dispatcher.dispatch(step)

    browser.actions.press.assert_awaited_once_with(
        "#searchInput",
        "Enter",
        timeout=30000,
    )

    assert step.selector == "{{search_selector}}"
