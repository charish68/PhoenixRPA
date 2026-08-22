from unittest.mock import AsyncMock, MagicMock

import pytest

from phoenixrpa.workflow.dispatcher import WorkflowDispatcher
from phoenixrpa.workflow.models import WorkflowStep
from phoenixrpa.workflow.variables import VariableResolver


@pytest.mark.asyncio
async def test_screenshot_resolves_variable_path():
    browser = MagicMock()
    browser.screenshots.capture_page = AsyncMock()

    variables = VariableResolver()
    variables.set(
        "screenshot_path",
        "screenshots/home.png",
    )

    dispatcher = WorkflowDispatcher(
        browser=browser,
        variables=variables,
        db=MagicMock(),
    )

    step = WorkflowStep(
        action="screenshot",
        path="{{screenshot_path}}",
    )

    await dispatcher.dispatch(step)

    browser.screenshots.capture_page.assert_awaited_once_with(
        "screenshots/home.png"
    )

    assert step.path == "{{screenshot_path}}"
