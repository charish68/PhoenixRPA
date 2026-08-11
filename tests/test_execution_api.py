from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from phoenixrpa.main import app


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
