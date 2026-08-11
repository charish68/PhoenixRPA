from pathlib import Path
from unittest.mock import MagicMock

from fastapi.testclient import TestClient

from phoenixrpa.main import app
from phoenixrpa.db.dependency import get_db


def test_screenshot_endpoint_returns_png(tmp_path):
    screenshot = tmp_path / "failure.png"
    screenshot.write_bytes(b"\x89PNG\r\n\x1a\nfake-png-data")

    fake_db = MagicMock()

    fake_log = MagicMock()
    fake_log.screenshot_path = str(screenshot)
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

        assert response.status_code == 200
        assert response.headers["content-type"] == "image/png"
        assert response.content.startswith(b"\x89PNG")

    finally:
        app.dependency_overrides.clear()
