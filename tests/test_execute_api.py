from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from phoenixrpa.main import app
from phoenixrpa.db.dependency import get_db


def test_execute_job_returns_404_when_job_missing():
    fake_db = MagicMock()

    app.dependency_overrides.clear()
    app.dependency_overrides[get_db] = lambda: fake_db

    try:
        with patch(
            "phoenixrpa.api.executor.JobRepository.get",
            return_value=None,
        ):
            client = TestClient(app)

            response = client.post(
                "/execute/999999"
            )

        assert response.status_code == 404
        assert response.json()["detail"] == "Job not found"

    finally:
        app.dependency_overrides.clear()
