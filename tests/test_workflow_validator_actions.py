from phoenixrpa.workflow.models import Workflow, WorkflowStep
from phoenixrpa.workflow.validator import WorkflowValidator


def test_validator_accepts_wait_text():
    workflow = Workflow(
        steps=[
            WorkflowStep(
                action="wait_text",
                value="Login successful",
            )
        ]
    )

    WorkflowValidator().validate(workflow)


def test_validator_accepts_extract_table():
    workflow = Workflow(
        steps=[
            WorkflowStep(
                action="extract_table",
                selector="#results",
                value="results_table",
            )
        ]
    )

    WorkflowValidator().validate(workflow)
def test_supported_actions_match_dispatcher_actions():
    from phoenixrpa.workflow.actions import SUPPORTED_ACTIONS

    expected_actions = {
        "goto",
        "click",
        "fill",
        "press",
        "hover",
        "wait_text",
        "wait_url",
        "wait_element",
        "extract_text",
        "extract_attribute",
        "extract_table",
        "extract_html",
        "screenshot",
        "if",
    }

    assert SUPPORTED_ACTIONS == expected_actions
import pytest

from phoenixrpa.workflow.models import Workflow, WorkflowStep
from phoenixrpa.workflow.validator import (
    WorkflowValidationError,
    WorkflowValidator,
)


def test_validator_rejects_unsupported_condition_operator():
    workflow = Workflow(
        steps=[
            WorkflowStep(
                action="if",
                condition="status > success",
            )
        ]
    )

    with pytest.raises(
        WorkflowValidationError,
        match="unsupported condition operator",
    ):
        WorkflowValidator().validate(workflow)
def test_validator_accepts_condition_with_spaced_right_value():
    workflow = Workflow(
        steps=[
            WorkflowStep(
                action="if",
                condition="{{status}} == 'Login successful'",
            )
        ]
    )

    WorkflowValidator().validate(workflow)
@pytest.mark.parametrize(
    "condition",
    [
        "status",
        "status ==",
        "== success",
    ],
)
def test_validator_rejects_malformed_conditions(
    condition,
):
    workflow = Workflow(
        steps=[
            WorkflowStep(
                action="if",
                condition=condition,
            )
        ]
    )

    with pytest.raises(
        WorkflowValidationError,
        match="Condition must contain left operator right",
    ):
        WorkflowValidator().validate(workflow)

def test_supported_actions_are_immutable():
    from phoenixrpa.workflow.actions import SUPPORTED_ACTIONS

    assert isinstance(
        SUPPORTED_ACTIONS,
        frozenset,
    )

@pytest.mark.parametrize(
    "timeout",
    [
        0,
        -1,
    ],
)
def test_validator_rejects_invalid_timeout(
    timeout,
):
    workflow = Workflow(
        steps=[
            WorkflowStep(
                action="goto",
                value="https://example.com",
                timeout=timeout,
            )
        ]
    )

    with pytest.raises(
        WorkflowValidationError,
        match="timeout must be greater than 0",
    ):
        WorkflowValidator().validate(workflow)


def test_validator_rejects_negative_retries():
    workflow = Workflow(
        steps=[
            WorkflowStep(
                action="goto",
                value="https://example.com",
                retries=-1,
            )
        ]
    )

    with pytest.raises(
        WorkflowValidationError,
        match="retries cannot be negative",
    ):
        WorkflowValidator().validate(workflow)