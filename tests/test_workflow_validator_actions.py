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

def test_validator_normalizes_action_name():
    workflow = Workflow(
        steps=[
            WorkflowStep(
                action="  CLICK  ",
                selector="#submit",
            )
        ]
    )

    WorkflowValidator().validate(workflow)




def test_validator_rejects_non_string_action():
    workflow = Workflow(
        steps=[
            WorkflowStep(
                action=123,
            )
        ]
    )

    with pytest.raises(
        WorkflowValidationError,
        match="action must be a string",
    ):
        WorkflowValidator().validate(workflow)


def test_validator_rejects_whitespace_only_action():
    workflow = Workflow(
        steps=[
            WorkflowStep(
                action="   ",
            )
        ]
    )

    with pytest.raises(
        WorkflowValidationError,
        match="action is required",
    ):
        WorkflowValidator().validate(workflow)

def test_validator_rejects_non_numeric_timeout():
    workflow = Workflow(
        steps=[
            WorkflowStep(
                action="goto",
                value="https://example.com",
                timeout="30000",
            )
        ]
    )

    with pytest.raises(
        WorkflowValidationError,
        match="timeout must be an integer",
    ):
        WorkflowValidator().validate(workflow)

def test_validator_rejects_non_numeric_retries():
    workflow = Workflow(
        steps=[
            WorkflowStep(
                action="goto",
                value="https://example.com",
                retries="2",
            )
        ]
    )

    with pytest.raises(
        WorkflowValidationError,
        match="retries must be an integer",
    ):
        WorkflowValidator().validate(workflow)

def test_validator_rejects_boolean_timeout():
    workflow = Workflow(
        steps=[
            WorkflowStep(
                action="goto",
                value="https://example.com",
                timeout=True,
            )
        ]
    )

    with pytest.raises(
        WorkflowValidationError,
        match="timeout must be an integer",
    ):
        WorkflowValidator().validate(workflow)
def test_validator_rejects_boolean_retries():
    workflow = Workflow(
        steps=[
            WorkflowStep(
                action="goto",
                value="https://example.com",
                retries=True,
            )
        ]
    )

    with pytest.raises(
        WorkflowValidationError,
        match="retries must be an integer",
    ):
        WorkflowValidator().validate(workflow)
def test_validator_rejects_boolean_retries():
    workflow = Workflow(
        steps=[
            WorkflowStep(
                action="goto",
                value="https://example.com",
                retries=True,
            )
        ]
    )

    with pytest.raises(
        WorkflowValidationError,
        match="retries must be an integer",
    ):
        WorkflowValidator().validate(workflow)                

def test_validator_rejects_nan_timeout():
    workflow = Workflow(
        steps=[
            WorkflowStep(
                action="goto",
                value="https://example.com",
                timeout=float("nan"),
            )
        ]
    )

    with pytest.raises(
        WorkflowValidationError,
        match="timeout must be an integer",
    ):
        WorkflowValidator().validate(workflow)

def test_validator_rejects_nan_retries():
    workflow = Workflow(
        steps=[
            WorkflowStep(
                action="goto",
                value="https://example.com",
                retries=float("nan"),
            )
        ]
    )

    with pytest.raises(
        WorkflowValidationError,
        match="retries must be an integer",
    ):
        WorkflowValidator().validate(workflow)

def test_validator_rejects_nan_retries():
    workflow = Workflow(
        steps=[
            WorkflowStep(
                action="goto",
                value="https://example.com",
                retries=float("nan"),
            )
        ]
    )

    with pytest.raises(
        WorkflowValidationError,
        match="retries must be an integer",
    ):
        WorkflowValidator().validate(workflow)

def test_validator_rejects_fractional_retries():
    workflow = Workflow(
        steps=[
            WorkflowStep(
                action="goto",
                value="https://example.com",
                retries=1.5,
            )
        ]
    )

    with pytest.raises(
        WorkflowValidationError,
        match="retries must be an integer",
    ):
        WorkflowValidator().validate(workflow)


def test_validator_rejects_fractional_timeout():
    workflow = Workflow(
        steps=[
            WorkflowStep(
                action="goto",
                value="https://example.com",
                timeout=1500.5,
            )
        ]
    )

    with pytest.raises(
        WorkflowValidationError,
        match="timeout must be an integer",
    ):
        WorkflowValidator().validate(workflow)


def test_validator_rejects_repeated_condition_operators():
    workflow = Workflow(
        steps=[
            WorkflowStep(
                action="if",
                condition="status == success == pending",
            )
        ]
    )

    with pytest.raises(
        WorkflowValidationError,
        match="Condition must contain exactly one operator",
    ):
        WorkflowValidator().validate(workflow)


def test_validator_rejects_repeated_not_equal_operators():
    workflow = Workflow(
        steps=[
            WorkflowStep(
                action="if",
                condition="status != success != pending",
            )
        ]
    )

    with pytest.raises(
        WorkflowValidationError,
        match="Condition must contain exactly one operator",
    ):
        WorkflowValidator().validate(workflow)

def test_validator_reports_invalid_true_branch_child_path():
    workflow = Workflow(
        steps=[
            WorkflowStep(
                action="if",
                condition="status == success",
                true_steps=[
                    WorkflowStep(
                        action="invalid_action",
                    )
                ],
            )
        ]
    )

    with pytest.raises(
        WorkflowValidationError,
        match=r"Step 1\.true\.1: unsupported action 'invalid_action'",
    ):
        WorkflowValidator().validate(workflow)


def test_validator_reports_invalid_false_branch_child_path():
    workflow = Workflow(
        steps=[
            WorkflowStep(
                action="if",
                condition="status == success",
                false_steps=[
                    WorkflowStep(
                        action="invalid_action",
                    )
                ],
            )
        ]
    )

    with pytest.raises(
        WorkflowValidationError,
        match=r"Step 1\.false\.1: unsupported action 'invalid_action'",
    ):
        WorkflowValidator().validate(workflow)

def test_validator_reports_deep_nested_branch_path():
    workflow = Workflow(
        steps=[
            WorkflowStep(
                action="if",
                condition="status == success",
                true_steps=[
                    WorkflowStep(
                        action="if",
                        condition="result == failed",
                        false_steps=[
                            WorkflowStep(
                                action="click",
                            )
                        ],
                    )
                ],
            )
        ]
    )

    with pytest.raises(
        WorkflowValidationError,
        match=(
            r"Step 1\.true\.1\.false\.1: "
            r"click requires 'selector'"
        ),
    ):
        WorkflowValidator().validate(workflow)

def test_validator_reports_nested_child_invalid_timeout():
    workflow = Workflow(
        steps=[
            WorkflowStep(
                action="if",
                condition="status == success",
                true_steps=[
                    WorkflowStep(
                        action="click",
                        selector="#login",
                        timeout=1500.5,
                    )
                ],
            )
        ]
    )

    with pytest.raises(
        WorkflowValidationError,
        match=(
            r"Step 1\.true\.1: "
            r"timeout must be an integer"
        ),
    ):
        WorkflowValidator().validate(workflow)


def test_validator_reports_nested_child_invalid_retries():
    workflow = Workflow(
        steps=[
            WorkflowStep(
                action="if",
                condition="status == success",
                false_steps=[
                    WorkflowStep(
                        action="click",
                        selector="#login",
                        retries=-1,
                    )
                ],
            )
        ]
    )

    with pytest.raises(
        WorkflowValidationError,
        match=(
            r"Step 1\.false\.1: "
            r"retries cannot be negative"
        ),
    ):
        WorkflowValidator().validate(workflow)

def test_validator_reports_nested_child_boolean_timeout():
    workflow = Workflow(
        steps=[
            WorkflowStep(
                action="if",
                condition="status == success",
                true_steps=[
                    WorkflowStep(
                        action="click",
                        selector="#login",
                        timeout=True,
                    )
                ],
            )
        ]
    )

    with pytest.raises(
        WorkflowValidationError,
        match=(
            r"Step 1\.true\.1: "
            r"timeout must be an integer"
        ),
    ):
        WorkflowValidator().validate(workflow)


def test_validator_reports_nested_child_boolean_retries():
    workflow = Workflow(
        steps=[
            WorkflowStep(
                action="if",
                condition="status == success",
                false_steps=[
                    WorkflowStep(
                        action="click",
                        selector="#login",
                        retries=False,
                    )
                ],
            )
        ]
    )

    with pytest.raises(
        WorkflowValidationError,
        match=(
            r"Step 1\.false\.1: "
            r"retries must be an integer"
        ),
    ):
        WorkflowValidator().validate(workflow)

def test_validator_reports_nested_invalid_condition_path():
    workflow = Workflow(
        steps=[
            WorkflowStep(
                action="if",
                condition="status == success",
                true_steps=[
                    WorkflowStep(
                        action="if",
                        condition="invalid_condition",
                    )
                ],
            )
        ]
    )

    with pytest.raises(
        WorkflowValidationError,
        match=(
            r"Step 1\.true\.1: "
            r"Condition must contain left operator right"
        ),
    ):
        WorkflowValidator().validate(workflow)

def test_validator_rejects_whitespace_only_condition():
    workflow = Workflow(
        steps=[
            WorkflowStep(
                action="if",
                condition="   ",
            )
        ]
    )

    with pytest.raises(
        WorkflowValidationError,
        match=r"Step 1: if requires 'condition'",
    ):
        WorkflowValidator().validate(workflow)


def test_validator_reports_nested_whitespace_only_condition():
    workflow = Workflow(
        steps=[
            WorkflowStep(
                action="if",
                condition="status == success",
                true_steps=[
                    WorkflowStep(
                        action="if",
                        condition="   ",
                    )
                ],
            )
        ]
    )

    with pytest.raises(
        WorkflowValidationError,
        match=(
            r"Step 1\.true\.1: "
            r"if requires 'condition'"
        ),
    ):
        WorkflowValidator().validate(workflow)

def test_validator_rejects_non_string_condition():
    workflow = Workflow(
        steps=[
            WorkflowStep(
                action="if",
                condition=123,
            )
        ]
    )

    with pytest.raises(
        WorkflowValidationError,
        match=r"Step 1: condition must be a string",
    ):
        WorkflowValidator().validate(workflow)

def test_validator_rejects_non_string_selector():
    workflow = Workflow(
        steps=[
            WorkflowStep(
                action="click",
                selector=123,
            )
        ]
    )

    with pytest.raises(
        WorkflowValidationError,
        match=r"Step 1: selector must be a string",
    ):
        WorkflowValidator().validate(workflow)
