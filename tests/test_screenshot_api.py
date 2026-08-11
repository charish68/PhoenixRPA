from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from phoenixrpa.main import app


def test_screenshot_endpoint_returns_404_when_no_screenshot():
    fake_db = MagicMock()

    fake_log = MagicMock()
    fake_log.screenshot_path = None

    fake_db.query.return_value.filter.return_value.first.return_value = (
        fake_log
    )

    app.dependency_overrides.clear()

    from phoenixrpa.db.dependency import get_db

    app.dependency_overrides[get_db] = lambda: fake_db

    try:
        client = TestClient(app)

        response = client.get(
            "/jobs/16/executions/123/screenshot"
        )

        assert response.status_code == 404
        assert response.json()["detail"] == (
            "No screenshot available for this execution"
        )

    finally:
        app.dependency_overrides.clear()
