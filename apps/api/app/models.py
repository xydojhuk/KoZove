from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    JSON,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.core import Base, utcnow


class Phone(Base):
    __tablename__ = "phone_numbers"

    id: Mapped[int] = mapped_column(primary_key=True)

    e164: Mapped[str] = mapped_column(
        String(20), unique=True, index=True
    )

    country: Mapped[str] = mapped_column(String(2), default="ME")
    number_type: Mapped[str] = mapped_column(
        String(32), default="unknown"
    )

    business_name: Mapped[str | None] = mapped_column(
        String(120), nullable=True
    )
    source_url: Mapped[str | None] = mapped_column(
        String(500), nullable=True
    )

    is_listed: Mapped[bool] = mapped_column(
        Boolean, default=False
    )

    created_at: Mapped[object] = mapped_column(
        DateTime(timezone=True), default=utcnow
    )


class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(primary_key=True)

    phone_id: Mapped[int] = mapped_column(
        ForeignKey("phone_numbers.id", ondelete="CASCADE"),
        index=True,
    )

    rating: Mapped[int] = mapped_column(Integer)
    category: Mapped[str] = mapped_column(String(40))
    body: Mapped[str] = mapped_column(Text)

    status: Mapped[str] = mapped_column(
        String(20), default="pending", index=True
    )

    risk_flags: Mapped[list] = mapped_column(
        JSON, default=list
    )

    fingerprint: Mapped[str] = mapped_column(String(64))

    created_at: Mapped[object] = mapped_column(
        DateTime(timezone=True), default=utcnow
    )
    moderated_at: Mapped[object | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )


class NumberReport(Base):
    __tablename__ = "number_reports"

    id: Mapped[int] = mapped_column(primary_key=True)

    phone_id: Mapped[int] = mapped_column(
        ForeignKey("phone_numbers.id", ondelete="CASCADE"),
        index=True,
    )

    category: Mapped[str] = mapped_column(String(40))
    body: Mapped[str] = mapped_column(Text, default="")

    status: Mapped[str] = mapped_column(
        String(20), default="pending", index=True
    )

    fingerprint: Mapped[str] = mapped_column(String(64))

    created_at: Mapped[object] = mapped_column(
        DateTime(timezone=True), default=utcnow
    )
    moderated_at: Mapped[object | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )


class Appeal(Base):
    __tablename__ = "appeals"

    id: Mapped[int] = mapped_column(primary_key=True)

    phone_e164: Mapped[str] = mapped_column(String(20))
    review_id: Mapped[int | None] = mapped_column(nullable=True)

    body: Mapped[str] = mapped_column(Text)
    contact_email: Mapped[str | None] = mapped_column(
        String(254), nullable=True
    )

    status: Mapped[str] = mapped_column(
        String(20), default="pending", index=True
    )

    created_at: Mapped[object] = mapped_column(
        DateTime(timezone=True), default=utcnow
    )


class AdminSession(Base):
    __tablename__ = "admin_sessions"

    id: Mapped[int] = mapped_column(primary_key=True)

    token_hash: Mapped[str] = mapped_column(
        String(64), unique=True, index=True
    )
    expires_at: Mapped[object] = mapped_column(
        DateTime(timezone=True)
    )


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(primary_key=True)

    action: Mapped[str] = mapped_column(String(60))
    target_type: Mapped[str] = mapped_column(String(40))
    target_id: Mapped[int | None] = mapped_column(nullable=True)

    created_at: Mapped[object] = mapped_column(
        DateTime(timezone=True), default=utcnow
    )


class AbuseEvent(Base):
    __tablename__ = "abuse_events"

    id: Mapped[int] = mapped_column(primary_key=True)

    fingerprint: Mapped[str] = mapped_column(String(64))
    action: Mapped[str] = mapped_column(String(30))

    created_at: Mapped[object] = mapped_column(
        DateTime(timezone=True), default=utcnow
    )

    __table_args__ = (
        Index(
            "ix_abuse_lookup",
            "fingerprint",
            "action",
            "created_at",
        ),
    )


class SystemState(Base):
    __tablename__ = "system_state"

    id: Mapped[int] = mapped_column(primary_key=True)
    mode: Mapped[str] = mapped_column(
        String(20), default="normal"
    )