from phoenixrpa.healing.models import HealingResult


def test_healing_result_includes_confidence():
    result = HealingResult(
        status="HEALED",
        original_selector="#userEmail",
        healed_selector="#emailInputChanged",
        method="AI",
        confidence=0.95,
    )

    assert result.confidence == 0.95

    assert result.to_dict() == {
        "status": "HEALED",
        "original_selector": "#userEmail",
        "healed_selector": "#emailInputChanged",
        "method": "AI",
        "confidence": 0.95,
    }
