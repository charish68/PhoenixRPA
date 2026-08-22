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