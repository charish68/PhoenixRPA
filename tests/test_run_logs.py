from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from phoenixrpa.main import app
from phoenixrpa.db.dependency import get_db


def test_get_run_logs_success():
    fake_db = MagicMock()

    fake_run = MagicMock()
    fake_run.id = 52

    fake_logs = [
        {
            "id": 227,
            "run_id": 52,
            "step_order": 1,
            "action": "if",
            "status": "SUCCESS",
        },
        {
            "id": 228,
            "run_id": 52,
            "step_order": 2,
            "action": "click",
            "status": "SUCCESS",
        },
    ]

    app.dependency_overrides.clear()
    app.dependency_overrides[get_db] = lambda: fake_db

    try:
        with patch(
            "phoenixrpa.api.execution.ExecutionService.list_runs",
            return_value=[fake_run],
        ), patch(
            "phoenixrpa.api.execution.ExecutionService.list_run_logs",
            return_value=fake_logs,
        ):
            client = TestClient(app)

            response = client.get(
                "/jobs/16/runs/52/logs"
            )

        assert response.status_code == 200

        body = response.json()

        assert len(body) == 2
        assert body[0]["run_id"] == 52
        assert body[0]["action"] == "if"
        assert body[1]["action"] == "click"

    finally:
        app.dependency_overrides.clear()
