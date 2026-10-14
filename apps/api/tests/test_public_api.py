
import pytest

from fastapi.testclient import TestClient
from sqlalchemy import func, select

from app import main
from app.core import get_db
from app.entrypoint import app
from app.models import (
    Appeal,
    NumberReport,
    Review,
)


@pytest.fixture()
def client(pg_session_factory, monkeypatch):
    monkeypatch.setattr(
        main,
        "normalize_number",
        lambda _: ("TEST-PHONE-API", "mobile"),
    )

    monkeypatch.setattr(
        main,
        "verify_turnstile",
        lambda token: None,
    )

    def database():
        with pg_session_factory() as db:
            yield db

    app.dependency_overrides[get_db] = database

    try:
        with TestClient(app) as c:
            yield c, pg_session_factory
    finally:
        app.dependency_overrides.clear()


def test_public_submissions_and_lookup(client):
    c, session_factory = client

    empty = c.get(
        "/api/v1/phone/lookup",
        params={"q": "synthetic"},
    )

    assert empty.status_code == 200
    assert empty.json()["found"] is False

    created = c.post(
        "/api/v1/reviews",
        json={
            "number": "synthetic",
            "rating": 4,
            "category": "normal",
            "text": "A synthetic test review",
            "turnstile_token": "test",
        },
    )

    assert created.status_code == 200
    assert created.json()["status"] == "pending"

    report_payload = {
        "number": "synthetic",
        "category": "other",
        "text": "Synthetic test report",
        "turnstile_token": "test",
    }

    report = c.post(
        "/api/v1/reports",
        json=report_payload,
    )

    assert report.status_code == 200

    second = c.post(
        "/api/v1/reports",
        json=report_payload,
    )

    assert second.status_code == 409

    appeal = c.post(
        "/api/v1/appeals",
        json={
            "number": "synthetic",
            "text":
                "Please review this synthetic entry",
            "turnstile_token": "test",
        },
    )

    assert appeal.status_code == 200

    with session_factory() as db:
        review = db.scalar(select(Review))

        assert review.status == "pending"

        assert db.scalar(
            select(func.count(NumberReport.id))
        ) == 1

        assert db.scalar(
            select(func.count(Appeal.id))
        ) == 1

        main.decide_pending(
            db,
            Review,
            review.id,
            "approved",
            "review",
        )

    found = c.get(
        "/api/v1/phone/lookup",
        params={"q": "synthetic"},
    )

    assert found.status_code == 200
    assert found.json()["found"] is True
    assert found.json()["rating_count"] == 1
    assert found.json()["rating"] is None
    assert len(found.json()["reviews"]) == 1
