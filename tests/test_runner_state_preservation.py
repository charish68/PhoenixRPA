from unittest.mock import AsyncMock, Mock

import pytest

from phoenixrpa.workflow.models import Workflow, WorkflowStep
from phoenixrpa.workflow.runner import WorkflowRunner


@pytest.mark.asyncio
async def test_runner_restores_original_step_values_after_success():
    browser = Mock()
    db = Mock()

    runner = WorkflowRunner(
        browser=browser,
        variables={
            "selector": "#resolved",
            "value": "resolved-value",
            "path": "resolved.png",
        },
        db=db,
    )

    dispatch = AsyncMock()
    runner.dispatcher.dispatch = dispatch

    step = WorkflowStep(
        action="click",
        selector="{{selector}}",
        value="{{value}}",
        path="{{path}}",
    )

    await runner.run_step(step)

    assert step.selector == "{{selector}}"
    assert step.value == "{{value}}"
    assert step.path == "{{path}}"

@pytest.mark.asyncio
async def test_runner_restores_original_step_values_after_failure():
    browser = Mock()
    db = Mock()

    runner = WorkflowRunner(
        browser=browser,
        variables={
            "selector": "#resolved",
            "value": "resolved-value",
            "path": "resolved.png",
        },
        db=db,
    )

    dispatch = AsyncMock(
        side_effect=RuntimeError("Dispatch failed")
    )
    runner.dispatcher.dispatch = dispatch

    step = WorkflowStep(
        action="click",
        selector="{{selector}}",
        value="{{value}}",
        path="{{path}}",
    )

    with pytest.raises(
        RuntimeError,
        match="Dispatch failed",
    ):
        await runner.run_step(step)

    assert step.selector == "{{selector}}"
    assert step.value == "{{value}}"
    assert step.path == "{{path}}"

@pytest.mark.asyncio
async def test_runner_restores_original_step_values_after_failure(monkeypatch):
    from phoenixrpa.workflow.runner import WorkflowRunner

    original_selector = "#username"
    original_value = "{{username}}"

    workflow = Workflow(
        steps=[
            WorkflowStep(
                action="fill",
                selector=original_selector,
                value=original_value,
            )
        ]
    )

    browser = Mock()
    db = Mock()
    runner = WorkflowRunner(browser=browser, db=db, variables={"username": "charish"})

    def fail_dispatch(*args, **kwargs):
        raise RuntimeError("Dispatch failed")

    monkeypatch.setattr(
        runner.dispatcher,
        "dispatch",
        fail_dispatch,
    )

    with pytest.raises(
        RuntimeError,
        match="Dispatch failed",
    ):
        await runner.run(workflow)

    step = workflow.steps[0]

    assert step.selector == original_selector
    assert step.value == original_value







@pytest.mark.asyncio
async def test_runner_stops_after_top_level_step_failure():
    browser = Mock()
    db = Mock()

    runner = WorkflowRunner(
        browser=browser,
        db=db,
    )

    first_step = WorkflowStep(
        action="click",
        selector="#first",
    )

    second_step = WorkflowStep(
        action="click",
        selector="#second",
    )

    workflow = Workflow(
        steps=[
            first_step,
            second_step,
        ]
    )

    dispatch = AsyncMock(
        side_effect=RuntimeError("First step failed")
    )

    runner.dispatcher.dispatch = dispatch

    with pytest.raises(
        RuntimeError,
        match="First step failed",
    ):
        await runner.run(workflow)

    assert dispatch.await_count == 1
