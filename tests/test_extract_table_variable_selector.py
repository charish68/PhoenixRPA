from unittest.mock import AsyncMock, MagicMock

import pytest

from phoenixrpa.workflow.dispatcher import WorkflowDispatcher
from phoenixrpa.workflow.models import WorkflowStep
from phoenixrpa.workflow.variables import VariableResolver


@pytest.mark.asyncio
async def test_extract_table_resolves_variable_selector():
    browser = MagicMock()

    expected_table = [
        ["Name", "Email"],
        ["Rahul", "rahul@example.com"],
    ]

    browser.extractor.table = AsyncMock(
        return_value=expected_table
    )

    variables = VariableResolver()
    variables.set(
        "table_selector",
        "#customersTable",
    )

    dispatcher = WorkflowDispatcher(
        browser=browser,
        variables=variables,
        db=MagicMock(),
    )

    step = WorkflowStep(
        action="extract_table",
        selector="{{table_selector}}",
        value="customers",
    )

    result = await dispatcher.dispatch(step)

    assert result == expected_table

    assert variables.resolve(
        "{{customers}}"
    ) == expected_table

    browser.extractor.table.assert_awaited_once_with(
        "#customersTable"
    )

    assert step.selector == "{{table_selector}}"
