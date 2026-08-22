from unittest.mock import AsyncMock, MagicMock

import pytest

from phoenixrpa.workflow.dispatcher import WorkflowDispatcher
from phoenixrpa.workflow.models import WorkflowStep
from phoenixrpa.workflow.variables import VariableResolver


@pytest.mark.asyncio
async def test_if_resolves_variable_on_both_sides():
    variables = VariableResolver()
    variables.set("status", "success")
    variables.set("expected_status", "success")

    dispatcher = WorkflowDispatcher(
        browser=MagicMock(),
        variables=variables,
        db=MagicMock(),
    )

    true_step = WorkflowStep(
        action="goto",
        value="https://example.com/true",
    )

    false_step = WorkflowStep(
        action="goto",
        value="https://example.com/false",
    )

    execute_child = AsyncMock()

    step = WorkflowStep(
        action="if",
        condition="{{status}} == {{expected_status}}",
        true_steps=[true_step],
        false_steps=[false_step],
    )

    await dispatcher.dispatch(
        step,
        execute_child=execute_child,
    )

    execute_child.assert_awaited_once_with(
        true_step,
        branch_path="true",
    )
