from unittest.mock import MagicMock

from fastapi.testclient import TestClient

from phoenixrpa.main import app
from phoenixrpa.db.dependency import get_db


def test_create_job_requires_name_and_target_site():
    fake_db = MagicMock()

    app.dependency_overrides.clear()
    app.dependency_overrides[get_db] = lambda: fake_db

    try:
        client = TestClient(app)

        response = client.post(
            "/jobs/",
            json={
                "name": "Only Name",
            },
        )

        assert response.status_code == 422

    finally:
        app.dependency_overrides.clear()
