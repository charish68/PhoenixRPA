from unittest.mock import AsyncMock, MagicMock

import pytest

from phoenixrpa.workflow.dispatcher import WorkflowDispatcher
from phoenixrpa.workflow.models import WorkflowStep
from phoenixrpa.workflow.variables import VariableResolver


@pytest.mark.asyncio
async def test_hover_resolves_variable_selector():
    browser = MagicMock()
    browser.actions.hover = AsyncMock()

    variables = VariableResolver()
    variables.set(
        "menu_selector",
        "#productsMenu",
    )

    dispatcher = WorkflowDispatcher(
        browser=browser,
        variables=variables,
        db=MagicMock(),
    )

    step = WorkflowStep(
        action="hover",
        selector="{{menu_selector}}",
    )

    await dispatcher.dispatch(step)

    browser.actions.hover.assert_awaited_once_with(
        "#productsMenu",
        timeout=30000,
    )

    assert step.selector == "{{menu_selector}}"
