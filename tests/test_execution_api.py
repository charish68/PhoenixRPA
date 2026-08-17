from types import SimpleNamespace
from unittest.mock import MagicMock, patch
import pytest
from fastapi.testclient import TestClient

from phoenixrpa.main import app
from phoenixrpa.db.dependency import get_db

def test_get_run_logs_returns_404_for_missing_run():
    fake_db = MagicMock()

    with patch(
        "phoenixrpa.api.execution.get_db",
        return_value=fake_db,
    ):
        client = TestClient(app)

        response = client.get(
            "/jobs/16/runs/999999/logs"
        )

    assert response.status_code == 404
    assert response.json()["detail"] == "Execution run not found"


def test_get_run_logs_returns_healing_metadata():
    fake_db = MagicMock()

    run = SimpleNamespace(
        id=52,
        job_id=16,
    )

    healed_log = SimpleNamespace(
        id=101,
        run_id=52,
        step_order=2,
        action="click",
        status="SUCCESS",
        healing_status="HEALED",
        original_selector="#userEmail",
        healed_selector="#emailInputChanged",
        healing_method="AI",
        healing_confidence=15 / 21,
    )

    app.dependency_overrides.clear()
    app.dependency_overrides[get_db] = lambda: fake_db

    try:
        with patch(
            "phoenixrpa.api.execution.ExecutionService.list_runs",
            return_value=[run],
        ), patch(
            "phoenixrpa.api.execution.ExecutionService.list_run_logs",
            return_value=[healed_log],
        ):
            client = TestClient(app)

            response = client.get(
                "/jobs/16/runs/52/logs"
            )

        assert response.status_code == 200

        logs = response.json()

        assert len(logs) == 1

        assert logs[0]["healing_status"] == "HEALED"
        assert logs[0]["original_selector"] == "#userEmail"
        assert logs[0]["healed_selector"] == "#emailInputChanged"
        assert logs[0]["healing_method"] == "AI"

        assert logs[0]["healing_confidence"] == pytest.approx(
            15 / 21
        )

    finally:
        app.dependency_overrides.clear()


def test_get_run_logs_returns_404_for_missing_run():
    fake_db = MagicMock()

    app.dependency_overrides.clear()
    app.dependency_overrides[get_db] = lambda: fake_db

    try:
        client = TestClient(app)

        response = client.get(
            "/jobs/16/runs/999999/logs"
        )

        assert response.status_code == 404
        assert response.json()["detail"] == "Execution run not found"

    finally:
        app.dependency_overrides.clear()