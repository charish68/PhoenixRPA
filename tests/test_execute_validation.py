from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from phoenixrpa.main import app
from phoenixrpa.db.dependency import get_db
from phoenixrpa.workflow.validator import WorkflowValidationError


def test_execute_job_returns_400_for_invalid_workflow():
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
            side_effect=WorkflowValidationError(
                "Workflow cannot be empty."
            ),
        ):
            client = TestClient(app)

            response = client.post(
                "/execute/16"
            )

        assert response.status_code == 400
        assert response.json()["detail"] == (
            "Workflow validation failed: Workflow cannot be empty."
        )

    finally:
        app.dependency_overrides.clear()
