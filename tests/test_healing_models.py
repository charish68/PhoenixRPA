from phoenixrpa.healing.models import HealingResult


def test_healing_result_deterministic():

    result = HealingResult(
        status="HEALED",
        original_selector="#userEmail",
        healed_selector="#emailInputChanged",
        method="DETERMINISTIC",
    )

    assert result.status == "HEALED"
    assert result.original_selector == "#userEmail"
    assert result.healed_selector == "#emailInputChanged"
    assert result.method == "DETERMINISTIC"


def test_healing_result_ai():

    result = HealingResult(
        status="HEALED",
        original_selector="#userEmail",
        healed_selector="#emailInputChanged",
        method="AI",
    )

    assert result.method == "AI"
