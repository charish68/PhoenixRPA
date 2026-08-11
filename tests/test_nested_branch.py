from unittest.mock import AsyncMock, MagicMock

import pytest

from phoenixrpa.workflow.dispatcher import WorkflowDispatcher
from phoenixrpa.workflow.models import WorkflowStep
from phoenixrpa.workflow.variables import VariableResolver


@pytest.mark.asyncio
async def test_nested_if_true_branch_builds_correct_path():
    browser = MagicMock()
    db = MagicMock()
    variables = VariableResolver()

    dispatcher = WorkflowDispatcher(
        browser=browser,
        variables=variables,
        db=db,
    )

    child = WorkflowStep(
        action="click",
        selector="#userName",
        timeout=30000,
    )

    nested_if = WorkflowStep(
        action="if",
        condition="success == success",
        timeout=30000,
    )

    nested_if.true_steps = [child]
    nested_if.false_steps = []

    root_if = WorkflowStep(
        action="if",
        condition="success == success",
        timeout=30000,
    )

    root_if.true_steps = [nested_if]
    root_if.false_steps = []

    executed = []

    async def execute_child(step, branch_path=None):
        executed.append(
            (step.action, branch_path)
        )

        if step.action == "if":
            await dispatcher.dispatch(
                step,
                execute_child=execute_child,
                branch_path=branch_path,
            )

    await dispatcher.dispatch(
        root_if,
        execute_child=execute_child,
    )

    assert executed == [
        ("if", "true"),
        ("click", "true.true"),
    ]
