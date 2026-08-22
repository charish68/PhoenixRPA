from unittest.mock import AsyncMock, MagicMock

import pytest

from phoenixrpa.workflow.dispatcher import WorkflowDispatcher
from phoenixrpa.workflow.models import WorkflowStep
from phoenixrpa.workflow.variables import VariableResolver


@pytest.mark.asyncio
async def test_extract_attribute_resolves_variable_selector():
    browser = MagicMock()

    browser.extractor.attribute = AsyncMock(
        return_value="https://example.com/profile"
    )

    variables = VariableResolver()
    variables.set(
        "profile_selector",
        "#profileLink",
    )

    dispatcher = WorkflowDispatcher(
        browser=browser,
        variables=variables,
        db=MagicMock(),
    )

    step = WorkflowStep(
        action="extract_attribute",
        selector="{{profile_selector}}",
        attribute="href",
        value="profile_url",
    )

    result = await dispatcher.dispatch(step)

    assert result == "https://example.com/profile"

    assert variables.resolve(
        "{{profile_url}}"
    ) == "https://example.com/profile"

    browser.extractor.attribute.assert_awaited_once_with(
        "#profileLink",
        "href",
    )
