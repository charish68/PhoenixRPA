from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from phoenixrpa.main import app
from phoenixrpa.db.dependency import get_db


def test_execute_job_returns_422_when_execution_fails():
    fake_db = MagicMock()

    fake_job = MagicMock()
    fake_job.id = 16

    app.dependency_overrides.clear()
    app.dependency_overrides[get_db] = lambda: fake_db

    try:
        with patch(
            "phoenixrpa.api.executor.JobRepository.get",
            return_value=fake_job,
        ), patch(
            "phoenixrpa.api.executor.JobExecutor.execute",
            side_effect=RuntimeError("browser execution failed"),
        ):
            client = TestClient(app)

            response = client.post(
                "/execute/16"
            )

        assert response.status_code == 422

        assert response.json()["detail"] == {
            "message": "Job execution failed",
            "error": "browser execution failed",
            "job_id": 16,
        }

    finally:
        app.dependency_overrides.clear()
