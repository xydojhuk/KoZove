from datetime import timedelta

from sqlalchemy import delete
from sqlalchemy.orm import Session

from app.core import SessionLocal, utcnow
from app.models import AbuseEvent, AdminSession


def cleanup(db: Session) -> tuple[int, int]:
    now = utcnow()

    expired_sessions = db.execute(
        delete(AdminSession).where(
            AdminSession.expires_at < now
        )
    ).rowcount

    old_events = db.execute(
        delete(AbuseEvent).where(
            AbuseEvent.created_at <
            now - timedelta(hours=48)
        )
    ).rowcount

    db.commit()

    return expired_sessions, old_events


if __name__ == "__main__":
    with SessionLocal() as db:
        sessions, events = cleanup(db)

    print(
        f"Deleted expired sessions: {sessions}; "
        f"old abuse events: {events}"
    )
