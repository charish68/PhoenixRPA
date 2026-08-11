from datetime import datetime
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from phoenixrpa.main import app
from phoenixrpa.db.dependency import get_db


def test_create_job_returns_created_job():
    fake_db = MagicMock()

    fake_job = SimpleNamespace(
        id=18,
        name="New Job",
        target_site="https://example.com",
        status="PENDING",
        created_at=datetime(2026, 8, 12, 12, 0, 0),
    )

    app.dependency_overrides.clear()
    app.dependency_overrides[get_db] = lambda: fake_db

    try:
        with patch(
            "phoenixrpa.api.jobs.JobService.create_job",
            return_value=fake_job,
        ):
            client = TestClient(app)

            response = client.post(
                "/jobs/",
                json={
                    "name": "New Job",
                    "target_site": "https://example.com",
                },
            )

        assert response.status_code == 200

        body = response.json()

        assert body["id"] == 18
        assert body["name"] == "New Job"
        assert body["target_site"] == "https://example.com"
        assert body["status"] == "PENDING"
        assert "created_at" in body

    finally:
        app.dependency_overrides.clear()
