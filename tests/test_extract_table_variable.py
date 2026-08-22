from unittest.mock import AsyncMock, MagicMock

import pytest

from phoenixrpa.workflow.dispatcher import WorkflowDispatcher
from phoenixrpa.workflow.models import WorkflowStep
from phoenixrpa.workflow.variables import VariableResolver


@pytest.mark.asyncio
async def test_extract_table_stores_workflow_variable():
    browser = MagicMock()

    table_data = [
        ["Name", "Amount"],
        ["Rahul", "1000"],
        ["Priya", "2000"],
    ]

    browser.extractor.table = AsyncMock(
        return_value=table_data
    )

    variables = VariableResolver()
    db = MagicMock()

    dispatcher = WorkflowDispatcher(
        browser=browser,
        variables=variables,
        db=db,
    )

    step = WorkflowStep(
        action="extract_table",
        selector="#transactions",
        value="transactions",
    )

    result = await dispatcher.dispatch(step)

    assert result == table_data

    assert variables.resolve(
        "{{transactions}}"
    ) == table_data

    browser.extractor.table.assert_awaited_once_with(
        "#transactions"
    )
