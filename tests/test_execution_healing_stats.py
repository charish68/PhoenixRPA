from unittest.mock import MagicMock
import pytest

from phoenixrpa.repositories.execution_repository import ExecutionRepository


def test_get_healing_stats():
    db = MagicMock()

    healed_ai = MagicMock()
    healed_ai.job_id = 16
    healed_ai.healing_status = "HEALED"
    healed_ai.healing_method = "AI"

    healed_other = MagicMock()
    healed_other.job_id = 16
    healed_other.healing_status = "HEALED"
    healed_other.healing_method = "DETERMINISTIC"

    normal = MagicMock()
    normal.job_id = 16
    normal.healing_status = "NONE"
    normal.healing_method = None

    query = db.query.return_value
    query.filter.return_value.all.return_value = [
        healed_ai,
        healed_other,
        normal,
    ]

    repository = ExecutionRepository(db)

    result = repository.get_healing_stats(16)

    assert result == {
        "total_steps": 3,
        "healed_steps": 2,
        "healing_rate": pytest.approx(66.66666666666667),
        "ai_healed": 1
    }
