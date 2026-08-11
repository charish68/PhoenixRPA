from datetime import datetime
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from phoenixrpa.main import app
from phoenixrpa.db.dependency import get_db


def test_list_jobs_returns_jobs():
    fake_db = MagicMock()

    fake_jobs = [
        SimpleNamespace(
            id=16,
            name="Job One",
            target_site="https://example.com",
            status="PENDING",
            created_at=datetime(2026, 8, 12, 12, 0, 0),
        ),
        SimpleNamespace(
            id=17,
            name="Job Two",
            target_site="https://example.org",
            status="SUCCESS",
            created_at=datetime(2026, 8, 12, 13, 0, 0),
        ),
    ]

    app.dependency_overrides.clear()
    app.dependency_overrides[get_db] = lambda: fake_db

    try:
        with patch(
            "phoenixrpa.api.jobs.JobService.list_jobs",
            return_value=fake_jobs,
        ):
            client = TestClient(app)

            response = client.get("/jobs/")

        assert response.status_code == 200

        body = response.json()

        assert len(body) == 2
        assert body[0]["id"] == 16
        assert body[0]["name"] == "Job One"
        assert body[1]["id"] == 17
        assert body[1]["name"] == "Job Two"

    finally:
        app.dependency_overrides.clear()
