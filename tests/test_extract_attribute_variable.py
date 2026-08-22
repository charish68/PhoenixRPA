from unittest.mock import AsyncMock, MagicMock

import pytest

from phoenixrpa.workflow.dispatcher import WorkflowDispatcher
from phoenixrpa.workflow.models import WorkflowStep
from phoenixrpa.workflow.variables import VariableResolver


@pytest.mark.asyncio
async def test_extract_attribute_stores_workflow_variable():
    browser = MagicMock()

    browser.extractor.attribute = AsyncMock(
        return_value="https://example.com/product/123"
    )

    variables = VariableResolver()
    db = MagicMock()

    dispatcher = WorkflowDispatcher(
        browser=browser,
        variables=variables,
        db=db,
    )

    step = WorkflowStep(
        action="extract_attribute",
        selector="#productLink",
        attribute="href",
        value="product_url",
    )

    result = await dispatcher.dispatch(step)

    assert result == "https://example.com/product/123"

    assert variables.resolve(
        "{{product_url}}"
    ) == "https://example.com/product/123"

    browser.extractor.attribute.assert_awaited_once_with(
        "#productLink",
        "href",
    )
