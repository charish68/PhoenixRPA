from unittest.mock import MagicMock

from phoenixrpa.repositories.execution_repository import ExecutionRepository


def test_mark_healed_persists_healing_method():
    db = MagicMock()
    log = MagicMock()

    repository = ExecutionRepository(db)

    result = repository.mark_healed(
        log,
        "#userEmail",
        "#emailInputChanged",
        "AI",
    )

    assert result is log
    assert log.healing_status == "HEALED"
    assert log.original_selector == "#userEmail"
    assert log.healed_selector == "#emailInputChanged"
    assert log.healing_method == "AI"

    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(log)
def test_mark_healed_persists_healing_confidence():
    db = MagicMock()
    log = MagicMock()

    repository = ExecutionRepository(db)

    result = repository.mark_healed(
        log,
        "#userEmail",
        "#emailInputChanged",
        "DETERMINISTIC",
        15 / 21,
    )

    assert result is log
    assert log.healing_status == "HEALED"
    assert log.original_selector == "#userEmail"
    assert log.healed_selector == "#emailInputChanged"
    assert log.healing_method == "DETERMINISTIC"
    assert log.healing_confidence == 15 / 21

    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(log)