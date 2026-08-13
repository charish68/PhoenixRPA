from unittest.mock import AsyncMock, MagicMock

import pytest

from phoenixrpa.healing.models import HealingResult
from phoenixrpa.workflow.dispatcher import WorkflowDispatcher
from phoenixrpa.workflow.models import WorkflowStep


@pytest.mark.asyncio
async def test_dispatcher_returns_healing_metadata():

    browser = MagicMock()
    variables = MagicMock()
    db = MagicMock()

    dispatcher = WorkflowDispatcher(
        browser=browser,
        variables=variables,
        db=db,
    )

    step = WorkflowStep(
        action="click",
        selector="#userEmail",
        step_order=1,
    )

    action = AsyncMock(
        side_effect=[
            RuntimeError("original selector failed"),
            None,
        ]
    )

    healing_result = HealingResult(
        status="HEALED",
        original_selector="#userEmail",
        healed_selector="#emailInputChanged",
        method="AI",
    )

    dispatcher.browser.healer.find_best_selector = AsyncMock(
        return_value=healing_result,
    )

    result = await dispatcher._execute_with_healing(
        step,
        action,
    )

    assert result == {
        "status": "HEALED",
        "original_selector": "#userEmail",
        "healed_selector": "#emailInputChanged",
        "method": "AI",
    }

    assert step.selector == "#emailInputChanged"
    assert action.await_count == 2

    dispatcher.browser.healer.find_best_selector.assert_awaited_once_with(
        "#userEmail",
        return_result=True,
    )
