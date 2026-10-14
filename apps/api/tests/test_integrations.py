
from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta

import pytest

from fastapi import HTTPException
from starlette.requests import Request
from sqlalchemy import func, select

from app import main
from app.antiabuse import (
    client_ip,
    fingerprint,
    rate_limit,
)
from app.cleanup import cleanup
from app.core import utcnow, settings
from app.models import (
    AbuseEvent,
    AdminSession,
    Appeal,
    NumberReport,
    Phone,
    Review,
)


def request(
    ip="192.0.2.15",
    agent="test-client",
    extra=None,
):
    headers = [
        (b"user-agent", agent.encode())
    ]

    headers.extend(
        (k.lower().encode(), v.encode())
        for k, v in (extra or {}).items()
    )

    return Request({
        "type": "http",
        "method": "POST",
        "path": "/api/v1/reviews",
        "headers": headers,
        "client": (ip, 40000),
        "server": ("127.0.0.1", 8000),
        "scheme": "http",
    })


def test_spoofed_ip_is_ignored():
    spoof = request(extra={
        "x-kozove-client-ip": "203.0.113.9",
        "x-kozove-proxy-secret": "wrong",
    })

    assert client_ip(spoof) == "192.0.2.15"
    assert fingerprint(spoof) == fingerprint(request())


def test_trusted_proxy_ip():
    req = request(extra={
        "x-kozove-client-ip": "203.0.113.9",
        "x-kozove-proxy-secret":
            settings.proxy_shared_secret,
    })

    assert client_ip(req) == "203.0.113.9"


def test_parallel_creates_one_phone(
    pg_session_factory,
    monkeypatch,
):
    monkeypatch.setattr(
        main,
        "normalize_number",
        lambda _: ("TEST-PHONE-001", "mobile"),
    )

    def create_one(_):
        with pg_session_factory() as db:
            phone = main.get_or_create_phone(
                db,
                "synthetic",
            )
            db.commit()
            return phone.id

    with ThreadPoolExecutor(max_workers=8) as pool:
        ids = list(
            pool.map(create_one, range(8))
        )

    assert len(set(ids)) == 1

    with pg_session_factory() as db:
        assert db.scalar(
            select(func.count(Phone.id))
        ) == 1


@pytest.mark.parametrize(
    "model,kind",
    [
        (Review, "review"),
        (NumberReport, "report"),
        (Appeal, "appeal"),
    ],
)
def test_only_one_moderation_decision(
    pg_session_factory,
    model,
    kind,
):
    with pg_session_factory() as db:
        phone = Phone(
            e164="TEST-PHONE-002",
            country="ME",
            number_type="mobile",
        )
        db.add(phone)
        db.flush()

        if model is Review:
            record = Review(
                phone_id=phone.id,
                rating=4,
                category="normal",
                body="Synthetic review text",
                status="pending",
                fingerprint="test",
                risk_flags=[],
            )

        elif model is NumberReport:
            record = NumberReport(
                phone_id=phone.id,
                category="other",
                body="Synthetic report",
                status="pending",
                fingerprint="test",
            )

        else:
            record = Appeal(
                phone_e164="TEST-PHONE-002",
                body="Synthetic appeal text",
                status="pending",
            )

        db.add(record)
        db.commit()

        item_id = record.id

    def decide(status):
        with pg_session_factory() as db:
            try:
                main.decide_pending(
                    db,
                    model,
                    item_id,
                    status,
                    kind,
                )
                return "ok"
            except HTTPException as exc:
                return exc.status_code

    first = (
        "resolved"
        if model is Appeal
        else "approved"
    )

    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(
            pool.map(decide, [first, "rejected"])
        )

    assert sorted(
        map(str, results)
    ) == ["409", "ok"]


def test_parallel_rate_limit(pg_session_factory):
    def attempt(_):
        with pg_session_factory() as db:
            try:
                rate_limit(
                    db,
                    request(),
                    "review",
                    2,
                    60,
                )
                db.commit()
                return "ok"
            except HTTPException as exc:
                return exc.status_code

    with ThreadPoolExecutor(max_workers=8) as pool:
        results = list(
            pool.map(attempt, range(8))
        )

    assert results.count("ok") == 2
    assert results.count(429) == 6


def test_cleanup(pg_session_factory):
    with pg_session_factory() as db:
        db.add(
            AdminSession(
                token_hash="test",
                expires_at=(
                    utcnow() - timedelta(days=1)
                ),
            )
        )

        db.add(
            AbuseEvent(
                fingerprint="test",
                action="review",
                created_at=(
                    utcnow() - timedelta(days=5)
                ),
            )
        )

        db.add(
            AbuseEvent(
                fingerprint="fresh",
                action="review",
                created_at=utcnow(),
            )
        )

        db.commit()

        assert cleanup(db) == (1, 1)

        assert db.scalar(
            select(func.count(AbuseEvent.id))
        ) == 1


def test_health_version():
    from app.entrypoint import app
    from fastapi.testclient import TestClient

    result = TestClient(app).get("/healthz")

    assert result.status_code == 200
    assert result.json()["version"] == settings.app_version
    assert app.version == settings.app_version


def test_live_routes_use_hardened_antiabuse():
    from app import antiabuse

    assert main.fingerprint is antiabuse.fingerprint
    assert main.rate_limit is antiabuse.rate_limit
