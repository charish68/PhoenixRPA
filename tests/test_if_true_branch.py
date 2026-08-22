from unittest.mock import AsyncMock, MagicMock

import pytest

from phoenixrpa.workflow.dispatcher import WorkflowDispatcher
from phoenixrpa.workflow.models import WorkflowStep
from phoenixrpa.workflow.variables import VariableResolver


@pytest.mark.asyncio
async def test_if_executes_true_branch():
    browser = MagicMock()

    variables = VariableResolver()
    variables.set(
        "status",
        "success",
    )

    dispatcher = WorkflowDispatcher(
        browser=browser,
        variables=variables,
        db=MagicMock(),
    )

    true_step = WorkflowStep(
        action="goto",
        value="https://example.com/success",
    )

    false_step = WorkflowStep(
        action="goto",
        value="https://example.com/failure",
    )

    dispatcher.dispatch = AsyncMock()

    step = WorkflowStep(
        action="if",
        condition="{{status}} == success",
        true_steps=[true_step],
        false_steps=[false_step],
    )

    await WorkflowDispatcher.dispatch(
        dispatcher,
        step,
    )

    dispatcher.dispatch.assert_awaited_once_with(
        true_step,
        branch_path="true",
    )
