from unittest.mock import MagicMock

import pytest

from phoenixrpa.workflow.dispatcher import WorkflowDispatcher
from phoenixrpa.workflow.models import WorkflowStep
from phoenixrpa.workflow.variables import VariableResolver


@pytest.mark.asyncio
async def test_nested_if_false_branch_builds_correct_path():
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
        selector="#userEmail",
        timeout=30000,
    )

    nested_if = WorkflowStep(
        action="if",
        condition="success == success",
        timeout=30000,
    )

    # Nested IF evaluates TRUE, so child belongs in TRUE branch.
    nested_if.true_steps = [child]
    nested_if.false_steps = []

    root_if = WorkflowStep(
        action="if",
        condition="success != success",
        timeout=30000,
    )

    # Root IF evaluates FALSE, so nested IF belongs here.
    root_if.true_steps = []
    root_if.false_steps = [nested_if]

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
        ("if", "false"),
        ("click", "false.true"),
    ]
