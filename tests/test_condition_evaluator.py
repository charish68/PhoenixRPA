import pytest

from phoenixrpa.workflow.condition import ConditionEvaluator


def test_condition_equals():
    evaluator = ConditionEvaluator()

    assert evaluator.evaluate(
        "success",
        "==",
        "success",
    ) is True


def test_condition_not_equals():
    evaluator = ConditionEvaluator()

    assert evaluator.evaluate(
        "success",
        "!=",
        "failed",
    ) is True


def test_condition_rejects_unsupported_operator():
    evaluator = ConditionEvaluator()

    with pytest.raises(
        ValueError,
        match="Unsupported condition operator",
    ):
        evaluator.evaluate(
            "10",
            ">",
            "5",
        )

def test_condition_with_values_containing_spaces():
    evaluator = ConditionEvaluator()

    assert evaluator.evaluate(
        "Login successful",
        "==",
        "Login successful",
    ) is True
@pytest.mark.parametrize(
    ("condition", "expected"),
    [
        (
            "{{status}} == {{expected_status}}",
            ("{{status}}", "==", "{{expected_status}}"),
        ),
        (
            "'Login successful' == {{status}}",
            ("'Login successful'", "==", "{{status}}"),
        ),
        (
            "{{status}} != 'Login failed'",
            ("{{status}}", "!=", "'Login failed'"),
        ),
    ],
)
def test_condition_parse(
    condition,
    expected,
):
    evaluator = ConditionEvaluator()

    assert evaluator.parse(condition) == expected
@pytest.mark.parametrize(
    "condition",
    [
        "status",
        "status ==",
        "== success",
    ],
)
def test_condition_parse_rejects_malformed_conditions(
    condition,
):
    evaluator = ConditionEvaluator()

    with pytest.raises(ValueError):
        evaluator.parse(condition)
