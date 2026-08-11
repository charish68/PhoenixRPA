from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from phoenixrpa.main import app
from phoenixrpa.db.dependency import get_db


def test_list_execution_runs():
    fake_db = MagicMock()

    run_one = MagicMock()
    run_one.id = 51
    run_one.job_id = 16
    run_one.status = "SUCCESS"

    run_two = MagicMock()
    run_two.id = 52
    run_two.job_id = 16
    run_two.status = "FAILED"

    app.dependency_overrides.clear()
    app.dependency_overrides[get_db] = lambda: fake_db

    try:
        with patch(
            "phoenixrpa.api.execution.ExecutionService.list_runs",
            return_value=[run_one, run_two],
        ):
            client = TestClient(app)

            response = client.get("/jobs/16/runs")

        assert response.status_code == 200

        body = response.json()

        assert len(body) == 2

    finally:
        app.dependency_overrides.clear()
