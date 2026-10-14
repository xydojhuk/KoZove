import hashlib
import hmac
import ipaddress

from datetime import timedelta

from fastapi import HTTPException, Request
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core import settings, utcnow
from app.models import AbuseEvent


def client_ip(request: Request) -> str:
    fallback = (
        request.client.host
        if request.client
        else "unknown"
    )

    presented = request.headers.get(
        "x-kozove-proxy-secret", ""
    )
    supplied = request.headers.get(
        "x-kozove-client-ip", ""
    )

    if not supplied or not hmac.compare_digest(
        presented,
        settings.proxy_shared_secret,
    ):
        return fallback

    try:
        return str(ipaddress.ip_address(supplied))
    except ValueError:
        return fallback


def fingerprint(request: Request) -> str:
    agent = request.headers.get(
        "user-agent", ""
    )[:200]

    data = f"{client_ip(request)}|{agent}".encode()

    return hmac.new(
        settings.abuse_pepper.encode(),
        data,
        hashlib.sha256,
    ).hexdigest()


def rate_limit(
    db: Session,
    request: Request,
    action: str,
    max_count: int,
    minutes: int,
) -> None:
    fp = fingerprint(request)

    lock_key = int.from_bytes(
        hashlib.sha256(
            f"{action}|{fp}".encode()
        ).digest()[:8],
        "big",
        signed=True,
    )

    db.execute(
        select(
            func.pg_advisory_xact_lock(lock_key)
        )
    )

    since = utcnow() - timedelta(
        minutes=minutes
    )

    count = db.scalar(
        select(func.count(AbuseEvent.id)).where(
            AbuseEvent.fingerprint == fp,
            AbuseEvent.action == action,
            AbuseEvent.created_at >= since,
        )
    ) or 0

    if count >= max_count:
        raise HTTPException(
            429,
            "Too many requests. Try again later.",
        )

    db.add(
        AbuseEvent(
            fingerprint=fp,
            action=action,
        )
    )

    db.flush()
