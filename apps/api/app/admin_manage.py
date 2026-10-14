from typing import Literal

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.core import get_db
from app.main import require_admin

from app.models import (
    Appeal,
    AuditLog,
    NumberReport,
    Phone,
    Review,
    SystemState,
)


router = APIRouter(
    prefix="/api/v1/admin/manage",
    dependencies=[Depends(require_admin)],
)


def count(db: Session, model, status: str | None = None) -> int:
    stmt = select(func.count(model.id))

    if status:
        stmt = stmt.where(model.status == status)

    return db.scalar(stmt) or 0


def paginate(db: Session, stmt, page: int, size: int, serialize):
    total = db.scalar(
        select(func.count()).select_from(
            stmt.order_by(None).subquery()
        )
    ) or 0

    rows = db.scalars(
        stmt.offset((page - 1) * size).limit(size)
    ).all()

    return {
        "items": [serialize(row) for row in rows],
        "total": total,
        "page": page,
        "size": size,
        "pages": max(1, (total + size - 1) // size),
    }


@router.get("/overview")
def overview(db: Session = Depends(get_db)):
    state = db.get(SystemState, 1)

    pending = db.scalars(
        select(Review)
        .where(Review.status == "pending")
        .order_by(Review.id.desc())
        .limit(4)
    ).all()

    return {
        "phones": count(db, Phone),

        "reviews": {
            s: count(db, Review, s)
            for s in ("pending", "approved", "rejected", "hidden")
        },

        "reports": {
            s: count(db, NumberReport, s)
            for s in ("pending", "approved", "rejected", "hidden")
        },

        "appeals": {
            s: count(db, Appeal, s)
            for s in ("pending", "resolved", "rejected")
        },

        "mode": state.mode if state else "normal",

        "latest_reviews": [
            {
                "id": r.id,
                "number": db.get(Phone, r.phone_id).e164,
                "text": r.body[:160],
                "rating": r.rating,
            }
            for r in pending
        ],
    }


@router.get("/reviews")
def reviews(
    status: Literal[
        "all", "pending", "approved", "rejected", "hidden"
    ] = "pending",
    q: str = "",
    page: int = Query(1, ge=1),
    size: int = Query(12, ge=1, le=50),
    db: Session = Depends(get_db),
):
    stmt = (
        select(Review)
        .join(Phone)
        .order_by(
            Review.created_at.desc(),
            Review.id.desc(),
        )
    )

    if status != "all":
        stmt = stmt.where(Review.status == status)

    if q.strip():
        pattern = f"%{q.strip()[:80]}%"

        stmt = stmt.where(
            or_(
                Phone.e164.ilike(pattern),
                Review.body.ilike(pattern),
            )
        )

    return paginate(
        db, stmt, page, size,
        lambda r: {
            "id": r.id,
            "number": db.get(Phone, r.phone_id).e164,
            "rating": r.rating,
            "category": r.category,
            "text": r.body,
            "status": r.status,
            "risk_flags": r.risk_flags,
            "created_at": r.created_at,
            "moderated_at": r.moderated_at,
        },
    )


@router.get("/reports")
def reports(
    status: Literal[
        "all", "pending", "approved", "rejected", "hidden"
    ] = "pending",
    q: str = "",
    page: int = Query(1, ge=1),
    size: int = Query(12, ge=1, le=50),
    db: Session = Depends(get_db),
):
    stmt = (
        select(NumberReport)
        .join(Phone)
        .order_by(
            NumberReport.created_at.desc(),
            NumberReport.id.desc(),
        )
    )

    if status != "all":
        stmt = stmt.where(NumberReport.status == status)

    if q.strip():
        pattern = f"%{q.strip()[:80]}%"

        stmt = stmt.where(
            or_(
                Phone.e164.ilike(pattern),
                NumberReport.body.ilike(pattern),
            )
        )

    return paginate(
        db, stmt, page, size,
        lambda r: {
            "id": r.id,
            "number": db.get(Phone, r.phone_id).e164,
            "category": r.category,
            "text": r.body,
            "status": r.status,
            "created_at": r.created_at,
            "moderated_at": r.moderated_at,
        },
    )


@router.get("/phones")
def phones(
    status: Literal[
        "all", "listed", "unlisted"
    ] = "all",
    q: str = "",
    page: int = Query(1, ge=1),
    size: int = Query(12, ge=1, le=50),
    db: Session = Depends(get_db),
):
    stmt = select(Phone).order_by(Phone.id.desc())

    if status != "all":
        stmt = stmt.where(
            Phone.is_listed.is_(status == "listed")
        )

    if q.strip():
        pattern = f"%{q.strip()[:80]}%"

        stmt = stmt.where(
            or_(
                Phone.e164.ilike(pattern),
                Phone.business_name.ilike(pattern),
            )
        )

    return paginate(
        db, stmt, page, size,
        lambda p: {
            "id": p.id,
            "number": p.e164,
            "business_name": p.business_name,
            "source_url": p.source_url,
            "is_listed": p.is_listed,
            "created_at": p.created_at,
        },
    )


@router.get("/appeals")
def appeals(
    status: Literal[
        "all", "pending", "resolved", "rejected"
    ] = "pending",
    q: str = "",
    page: int = Query(1, ge=1),
    size: int = Query(12, ge=1, le=50),
    db: Session = Depends(get_db),
):
    stmt = select(Appeal).order_by(Appeal.id.desc())

    if status != "all":
        stmt = stmt.where(Appeal.status == status)

    if q.strip():
        pattern = f"%{q.strip()[:80]}%"

        stmt = stmt.where(
            or_(
                Appeal.phone_e164.ilike(pattern),
                Appeal.body.ilike(pattern),
            )
        )

    return paginate(
        db, stmt, page, size,
        lambda a: {
            "id": a.id,
            "number": a.phone_e164,
            "review_id": a.review_id,
            "text": a.body,
            "contact_email": a.contact_email,
            "status": a.status,
            "created_at": a.created_at,
        },
    )


@router.get("/audit")
def audit_log(
    q: str = "",
    page: int = Query(1, ge=1),
    size: int = Query(12, ge=1, le=50),
    db: Session = Depends(get_db),
):
    stmt = select(AuditLog).order_by(AuditLog.id.desc())

    if q.strip():
        pattern = f"%{q.strip()[:80]}%"

        stmt = stmt.where(
            or_(
                AuditLog.action.ilike(pattern),
                AuditLog.target_type.ilike(pattern),
            )
        )

    return paginate(
        db, stmt, page, size,
        lambda a: {
            "id": a.id,
            "action": a.action,
            "target_type": a.target_type,
            "target_id": a.target_id,
            "created_at": a.created_at,
        },
    )
