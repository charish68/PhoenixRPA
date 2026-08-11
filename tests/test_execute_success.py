from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from phoenixrpa.main import app
from phoenixrpa.db.dependency import get_db


def test_execute_job_returns_success():
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
            return_value=None,
        ):
            client = TestClient(app)

            response = client.post(
                "/execute/16",
                json={
                    "variables": {
                        "username": "testuser"
                    }
                },
            )

        assert response.status_code == 200

        assert response.json() == {
            "message": "Job completed",
            "job_id": 16,
            "status": "COMPLETED",
        }

    finally:
        app.dependency_overrides.clear()
