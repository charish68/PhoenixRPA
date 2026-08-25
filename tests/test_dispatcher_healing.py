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
        "confidence": None,
    }

    assert step.selector == "#emailInputChanged"
    assert action.await_count == 2

    dispatcher.browser.healer.find_best_selector.assert_awaited_once_with(
        "#userEmail",
        return_result=True,
    )

@pytest.mark.asyncio
async def test_dispatcher_restores_variable_selector_after_healing():

    browser = MagicMock()
    variables = MagicMock()
    db = MagicMock()

    variables.resolve.side_effect = (
        lambda value: "#userEmail"
        if value == "{{email_selector}}"
        else value
    )

    dispatcher = WorkflowDispatcher(
        browser=browser,
        variables=variables,
        db=db,
    )

    step = WorkflowStep(
        action="click",
        selector="{{email_selector}}",
        step_order=1,
    )

    dispatcher.browser.actions.click = AsyncMock(
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

    result = await dispatcher.dispatch(step)

    assert result is not None
    assert result["healed_selector"] == "#emailInputChanged"

    assert step.selector == "{{email_selector}}"

    assert dispatcher.browser.actions.click.await_count == 2

    dispatcher.browser.actions.click.assert_any_await(
        "#userEmail",
        timeout=step.timeout,
    )

    dispatcher.browser.actions.click.assert_any_await(
        "#emailInputChanged",
        timeout=step.timeout,
    )

@pytest.mark.asyncio
async def test_dispatcher_restores_selector_when_action_fails():

    browser = MagicMock()
    variables = MagicMock()
    db = MagicMock()

    variables.resolve.side_effect = (
        lambda value: "#resolvedButton"
        if value == "{{button}}"
        else value
    )

    dispatcher = WorkflowDispatcher(
        browser=browser,
        variables=variables,
        db=db,
    )

    step = WorkflowStep(
        action="click",
        selector="{{button}}",
    )

    dispatcher.browser.actions.click = AsyncMock(
        side_effect=RuntimeError("click failed")
    )

    dispatcher.browser.healer.find_best_selector = AsyncMock(
        return_value=None
    )

    with pytest.raises(RuntimeError, match="click failed"):
        await dispatcher.dispatch(step)

    assert step.selector == "{{button}}"
