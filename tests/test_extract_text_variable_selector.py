from unittest.mock import AsyncMock, MagicMock

import pytest

from phoenixrpa.workflow.dispatcher import WorkflowDispatcher
from phoenixrpa.workflow.models import WorkflowStep
from phoenixrpa.workflow.variables import VariableResolver


@pytest.mark.asyncio
async def test_extract_text_resolves_variable_selector():
    browser = MagicMock()

    browser.extractor.text = AsyncMock(
        return_value="Rahul Kumar"
    )

    variables = VariableResolver()
    variables.set(
        "customer_selector",
        "#customerName",
    )

    dispatcher = WorkflowDispatcher(
        browser=browser,
        variables=variables,
        db=MagicMock(),
    )

    step = WorkflowStep(
        action="extract_text",
        selector="{{customer_selector}}",
        value="customer_name",
    )

    result = await dispatcher.dispatch(step)

    assert result == "Rahul Kumar"

    assert variables.resolve(
        "{{customer_name}}"
    ) == "Rahul Kumar"

    browser.extractor.text.assert_awaited_once_with(
        "#customerName"
    )
