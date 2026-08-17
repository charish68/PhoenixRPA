from phoenixrpa.healing.models import HealingResult


def test_healing_result_includes_failure_reason():

    result = HealingResult(
        status="FAILED",
        original_selector="#userEmail",
        method="AI",
        failure_reason="AI_VALIDATION_FAILED",
    )

    assert result.failure_reason == "AI_VALIDATION_FAILED"

    assert result.to_dict() == {
        "status": "FAILED",
        "original_selector": "#userEmail",
        "healed_selector": None,
        "method": "AI",
        "confidence": None,
        "failure_reason": "AI_VALIDATION_FAILED",
    }
