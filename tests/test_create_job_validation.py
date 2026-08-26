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

import pytest


@pytest.mark.parametrize(
    "payload",
    [
        {
            "name": "",
            "target_site": "https://example.com",
        },
        {
            "name": "   ",
            "target_site": "https://example.com",
        },
        {
            "name": "Valid Job",
            "target_site": "",
        },
        {
            "name": "Valid Job",
            "target_site": "   ",
        },
    ],
)
def test_create_job_rejects_empty_or_whitespace_fields(payload):
    fake_db = MagicMock()

    app.dependency_overrides.clear()
    app.dependency_overrides[get_db] = lambda: fake_db

    try:
        client = TestClient(app)

        response = client.post(
            "/jobs/",
            json=payload,
        )

        assert response.status_code == 422

    finally:
        app.dependency_overrides.clear()
import pytest
from unittest.mock import MagicMock

from fastapi.testclient import TestClient

from phoenixrpa.main import app
from phoenixrpa.db.dependency import get_db


@pytest.mark.parametrize(
    "payload",
    [
        {
            "name": 123,
            "target_site": "https://example.com",
        },
        {
            "name": "Test Job",
            "target_site": 123,
        },
        {
            "name": None,
            "target_site": "https://example.com",
        },
        {
            "name": "Test Job",
            "target_site": None,
        },
    ],
)
def test_create_job_rejects_invalid_field_types(payload):
    fake_db = MagicMock()

    app.dependency_overrides.clear()
    app.dependency_overrides[get_db] = lambda: fake_db

    try:
        client = TestClient(app)

        response = client.post(
            "/jobs/",
            json=payload,
        )

        assert response.status_code == 422

    finally:
        app.dependency_overrides.clear()
