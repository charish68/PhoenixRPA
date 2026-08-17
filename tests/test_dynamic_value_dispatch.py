from datetime import date, timedelta
from unittest.mock import AsyncMock, MagicMock

import pytest

from phoenixrpa.workflow.dispatcher import WorkflowDispatcher
from phoenixrpa.workflow.models import WorkflowStep
from phoenixrpa.workflow.variables import VariableResolver


@pytest.mark.asyncio
async def test_fill_resolves_dynamic_date_value():
    browser = MagicMock()

    browser.actions.fill = AsyncMock()

    browser.healer.find_best_selector = AsyncMock(
        side_effect=AssertionError(
            "Healing should not be called"
        )
    )

    variables = VariableResolver()
    db = MagicMock()

    dispatcher = WorkflowDispatcher(
        browser=browser,
        variables=variables,
        db=db,
    )

    step = WorkflowStep(
        action="fill",
        selector="#fromDate",
        value="{{TODAY-7}}",
    )

    await dispatcher.dispatch(step)

    expected = (
        date.today() - timedelta(days=7)
    ).isoformat()

    browser.actions.fill.assert_awaited_once_with(
        "#fromDate",
        expected,
        timeout=step.timeout,
    )
