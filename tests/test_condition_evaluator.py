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