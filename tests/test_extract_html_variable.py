from unittest.mock import AsyncMock, MagicMock

import pytest

from phoenixrpa.workflow.dispatcher import WorkflowDispatcher
from phoenixrpa.workflow.models import WorkflowStep
from phoenixrpa.workflow.variables import VariableResolver


@pytest.mark.asyncio
async def test_extract_html_stores_workflow_variable():
    browser = MagicMock()

    html = (
        "<html><body>"
        "<h1>Welcome</h1>"
        "</body></html>"
    )

    browser.extractor.html = AsyncMock(
        return_value=html
    )

    variables = VariableResolver()
    db = MagicMock()

    dispatcher = WorkflowDispatcher(
        browser=browser,
        variables=variables,
        db=db,
    )

    step = WorkflowStep(
        action="extract_html",
        value="page_html",
    )

    result = await dispatcher.dispatch(step)

    assert result == html

    assert variables.resolve(
        "{{page_html}}"
    ) == html

    browser.extractor.html.assert_awaited_once()
