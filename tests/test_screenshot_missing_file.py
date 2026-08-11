from unittest.mock import MagicMock

from fastapi.testclient import TestClient

from phoenixrpa.main import app
from phoenixrpa.db.dependency import get_db


def test_screenshot_endpoint_returns_404_when_file_missing():
    fake_db = MagicMock()

    fake_log = MagicMock()
    fake_log.screenshot_path = "recorded/failures/does_not_exist.png"
    fake_log.id = 123
    fake_log.job_id = 16

    fake_db.query.return_value.filter.return_value.first.return_value = (
        fake_log
    )

    app.dependency_overrides.clear()
    app.dependency_overrides[get_db] = lambda: fake_db

    try:
        client = TestClient(app)

        response = client.get(
            "/jobs/16/executions/123/screenshot"
        )

        assert response.status_code == 404
        assert response.json()["detail"] == (
            "Screenshot file not found"
        )

    finally:
        app.dependency_overrides.clear()
