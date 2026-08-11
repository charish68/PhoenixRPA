from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from phoenixrpa.main import app
from phoenixrpa.db.dependency import get_db


def test_get_run_logs_returns_404_when_run_missing():
    fake_db = MagicMock()

    app.dependency_overrides.clear()
    app.dependency_overrides[get_db] = lambda: fake_db

    try:
        with patch(
            "phoenixrpa.api.execution.ExecutionService.list_runs",
            return_value=[],
        ):
            client = TestClient(app)

            response = client.get(
                "/jobs/16/runs/999999/logs"
            )

        assert response.status_code == 404
        assert response.json()["detail"] == (
            "Execution run not found"
        )

    finally:
        app.dependency_overrides.clear()
