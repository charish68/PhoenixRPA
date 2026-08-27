from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from phoenixrpa.main import app
from phoenixrpa.db.dependency import get_db


def test_delete_job_success():
    fake_db = MagicMock()

    app.dependency_overrides.clear()
    app.dependency_overrides[get_db] = lambda: fake_db

    try:
        with patch(
            "phoenixrpa.api.jobs.JobService.delete_job",
            return_value=True,
        ):
            client = TestClient(app)

            response = client.delete("/jobs/16")

        assert response.status_code == 200
        assert response.json() == {
            "message": "Job deleted successfully"
        }

    finally:
        app.dependency_overrides.clear()

import pytest


@pytest.mark.parametrize(
    "job_id",
    [
        0,
        -1,
        -100,
    ],
)
def test_delete_job_rejects_non_positive_id(job_id):
    fake_db = MagicMock()

    app.dependency_overrides.clear()
    app.dependency_overrides[get_db] = lambda: fake_db

    try:
        client = TestClient(app)

        response = client.delete(
            f"/jobs/{job_id}"
        )

        assert response.status_code == 422

    finally:
        app.dependency_overrides.clear()

@pytest.mark.parametrize(
    "job_id",
    [
        "abc",
        "1.5",
        "true",
    ],
)
def test_delete_job_rejects_non_integer_id(job_id):
    fake_db = MagicMock()

    app.dependency_overrides.clear()
    app.dependency_overrides[get_db] = lambda: fake_db

    try:
        client = TestClient(app)

        response = client.delete(
            f"/jobs/{job_id}"
        )

        assert response.status_code == 422

    finally:
        app.dependency_overrides.clear()
