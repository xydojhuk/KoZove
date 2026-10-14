import hashlib
import re
import secrets

from datetime import timedelta
from typing import Literal

import httpx
import phonenumbers

from argon2 import PasswordHasher
from fastapi import Depends, FastAPI, HTTPException, Request, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import func, select, update
from app.antiabuse import fingerprint, rate_limit
from sqlalchemy.orm import Session

from app.core import get_db, settings, utcnow
from app.models import (
    Phone,
    Review,
    NumberReport,
    Appeal,
    AdminSession,
    AuditLog,
    SystemState,
)


app = FastAPI(
    title="KoZove API",
    version=settings.app_version,
)

hasher = PasswordHasher()
COOKIE_NAME = "kozove_admin"


# -----------------------
# Input schemas
# -----------------------

class ReviewInput(BaseModel):
    number: str = Field(min_length=6, max_length=40)
    rating: int = Field(ge=1, le=5)
    category: Literal[
        "normal", "delivery", "ads",
        "survey", "suspicious", "robot", "other"
    ]
    text: str = Field(min_length=10, max_length=600)
    turnstile_token: str = Field(min_length=1)


class ReportInput(BaseModel):
    number: str = Field(min_length=6, max_length=40)
    category: Literal[
        "scam", "ads", "harassment",
        "data", "robot", "other"
    ]
    text: str = Field(default="", max_length=600)
    turnstile_token: str = Field(min_length=1)


class AppealInput(BaseModel):
    number: str
    text: str = Field(min_length=10, max_length=1500)
    review_id: int | None = None
    contact_email: EmailStr | None = Field(
        default=None,
        max_length=254,
    )
    turnstile_token: str = Field(min_length=1)


class LoginInput(BaseModel):
    username: str
    password: str


class PhoneInput(BaseModel):
    number: str
    business_name: str | None = Field(default=None, max_length=120)
    source_url: str | None = Field(default=None, max_length=500)


class PhoneEdit(BaseModel):
    business_name: str | None = Field(default=None, max_length=120)
    source_url: str | None = Field(default=None, max_length=500)


class Decision(BaseModel):
    status: Literal["approved", "rejected", "hidden"]


class AppealDecision(BaseModel):
    status: Literal["resolved", "rejected"]


class MaintenanceInput(BaseModel):
    mode: Literal["normal", "read_only", "maintenance"]


# -----------------------
# Security and helpers
# -----------------------

@app.middleware("http")
async def security_headers(request: Request, call_next):
    if request.method not in ("GET", "HEAD", "OPTIONS"):
        origin = request.headers.get("origin")

        if origin and origin != settings.public_origin:
            return JSONResponse(
                {"detail": "Origin not allowed"},
                status_code=403,
            )

    response = await call_next(request)

    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["X-Frame-Options"] = "DENY"

    if request.url.path.startswith("/api/v1/admin/"):
        response.headers["Cache-Control"] = "no-store"

    return response


def normalize_number(raw: str):
    try:
        parsed = phonenumbers.parse(raw, "ME")
    except phonenumbers.NumberParseException:
        raise HTTPException(422, "Invalid phone number")

    if parsed.country_code != 382:
        raise HTTPException(422, "Only Montenegro is supported")

    if not phonenumbers.is_valid_number(parsed):
        raise HTTPException(422, "Invalid phone number")

    e164 = phonenumbers.format_number(
        parsed,
        phonenumbers.PhoneNumberFormat.E164,
    )

    kind = phonenumbers.number_type(parsed)

    mobile_types = {
        phonenumbers.PhoneNumberType.MOBILE,
        phonenumbers.PhoneNumberType.FIXED_LINE_OR_MOBILE,
    }

    number_type = (
        "mobile" if kind in mobile_types
        else "landline"
        if kind == phonenumbers.PhoneNumberType.FIXED_LINE
        else "other"
    )

    return e164, number_type



def verify_turnstile(token: str):
    try:
        response = httpx.post(
            "https://challenges.cloudflare.com/turnstile/v0/siteverify",
            data={
                "secret": settings.turnstile_secret,
                "response": token,
            },
            timeout=7,
        )

        response.raise_for_status()
        result = response.json()

    except (httpx.HTTPError, ValueError):
        raise HTTPException(
            503,
            "Anti-bot verification temporarily unavailable",
        )

    if not result.get("success"):
        raise HTTPException(403, "Anti-bot verification failed")


def inspect_text(text: str):
    flags = []

    rules = {
        "email": r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}",
        "url": r"(?:https?://|www\.)\S+",
        "phone": r"(?<!\w)\+?\d[\d().\s-]{7,}\d(?!\w)",
        "address": (
            r"\b(?:улица|вулиця|ул\.|адрес|adresa|"
            r"ulica|street)\s+[\w\s.-]{2,50}\d+\b"
        ),
        "possible_name": (
            r"\b[А-ЯЁІЇЄ][а-яёіїє']+\s+"
            r"[А-ЯЁІЇЄ][а-яёіїє']+\s+"
            r"[А-ЯЁІЇЄ][а-яёіїє']+\b"
        ),
    }

    for flag, pattern in rules.items():
        if re.search(pattern, text, re.IGNORECASE if flag != "possible_name" else 0):
            flags.append(flag)

    return flags


def check_write_mode(db: Session):
    state = db.get(SystemState, 1)

    if state and state.mode != "normal":
        raise HTTPException(
            503,
            "New submissions are temporarily disabled",
        )


def check_read_mode(db: Session):
    state = db.get(SystemState, 1)

    if state and state.mode == "maintenance":
        raise HTTPException(503, "Site under maintenance")



def get_or_create_phone(
    db: Session,
    number: str,
) -> Phone:
    from sqlalchemy.dialects.postgresql import (
        insert as pg_insert
    )

    e164, number_type = normalize_number(number)

    stmt = (
        pg_insert(Phone)
        .values(
            e164=e164,
            country="ME",
            number_type=number_type,
            is_listed=False,
        )
        .on_conflict_do_nothing(
            index_elements=[Phone.e164]
        )
        .returning(Phone.id)
    )

    phone_id = db.scalar(stmt)

    if phone_id is None:
        phone_id = db.scalar(
            select(Phone.id).where(
                Phone.e164 == e164
            )
        )

    if phone_id is None:
        raise HTTPException(
            503,
            "Phone record temporarily unavailable",
        )

    return db.get(Phone, phone_id)


def audit(
    db: Session,
    action: str,
    target_type: str,
    target_id: int | None,
):
    db.add(AuditLog(
        action=action,
        target_type=target_type,
        target_id=target_id,
    ))


def decide_pending(
    db: Session,
    model,
    object_id: int,
    status: str,
    kind: str,
) -> dict:
    values = {"status": status}

    if model in (Review, NumberReport):
        values["moderated_at"] = utcnow()

    decided_id = db.scalar(
        update(model)
        .where(
            model.id == object_id,
            model.status == "pending",
        )
        .values(**values)
        .returning(model.id)
    )

    if decided_id is None:
        if db.get(model, object_id) is None:
            raise HTTPException(
                404,
                f"{kind.capitalize()} not found",
            )

        raise HTTPException(
            409,
            "This item was already moderated; refresh the list",
        )

    audit(db, status, kind, object_id)
    db.commit()

    return {"ok": True}


def require_admin(
    request: Request,
    db: Session = Depends(get_db),
):
    if request.method not in ("GET", "HEAD"):
        if request.headers.get("x-kozove-admin") != "1":
            raise HTTPException(403, "Missing admin request header")

    token = request.cookies.get(COOKIE_NAME)

    if not token:
        raise HTTPException(401, "Not authenticated")

    token_hash = hashlib.sha256(token.encode()).hexdigest()

    session = db.scalar(
        select(AdminSession).where(
            AdminSession.token_hash == token_hash,
            AdminSession.expires_at > utcnow(),
        )
    )

    if session is None:
        raise HTTPException(401, "Session expired")

    return True


# -----------------------
# Public endpoints
# -----------------------


@app.get("/healthz")
def healthz():
    return {
        "status": "ok",
        "version": settings.app_version,
    }


@app.get("/api/v1/phone/lookup")
def lookup_phone(
    q: str,
    db: Session = Depends(get_db),
):
    check_read_mode(db)

    e164, number_type = normalize_number(q)

    phone = db.scalar(
        select(Phone).where(Phone.e164 == e164)
    )

    empty = {
        "found": False,
        "number": e164,
        "number_type": number_type,
        "business_name": None,
        "source_url": None,
        "rating": None,
        "rating_count": 0,
        "complaints": 0,
        "has_warnings": False,
        "reviews": [],
    }

    if phone is None:
        return empty

    reviews = db.scalars(
        select(Review)
        .where(
            Review.phone_id == phone.id,
            Review.status == "approved",
        )
        .order_by(Review.created_at.desc())
        .limit(50)
    ).all()

    rating_data = db.execute(
        select(
            func.count(Review.id),
            func.avg(Review.rating),
        ).where(
            Review.phone_id == phone.id,
            Review.status == "approved",
        )
    ).one()

    rating_count = rating_data[0] or 0
    average = rating_data[1]

    complaints = db.scalar(
        select(func.count(NumberReport.id)).where(
            NumberReport.phone_id == phone.id,
            NumberReport.status == "approved",
        )
    ) or 0

    public = (
        phone.is_listed
        or rating_count > 0
        or complaints > 0
    )

    if not public:
        return empty

    return {
        "found": True,
        "number": e164,
        "number_type": phone.number_type,
        "business_name": phone.business_name,
        "source_url": phone.source_url,
        "rating": (
            round(float(average), 1)
            if rating_count >= 3 and average is not None
            else None
        ),
        "rating_count": rating_count,
        "complaints": complaints,
        "has_warnings": False,
        "reviews": [
            {
                "id": r.id,
                "rating": r.rating,
                "category": r.category,
                "text": r.body,
                "created_at": r.created_at,
            }
            for r in reviews
        ],
    }


@app.post("/api/v1/reviews")
def submit_review(
    payload: ReviewInput,
    request: Request,
    db: Session = Depends(get_db),
):
    check_write_mode(db)
    verify_turnstile(payload.turnstile_token)

    rate_limit(db, request, "review", 5, 60)

    phone = get_or_create_phone(db, payload.number)

    body = payload.text.strip()

    review = Review(
        phone_id=phone.id,
        rating=payload.rating,
        category=payload.category,
        body=body,
        status="pending",
        risk_flags=inspect_text(body),
        fingerprint=fingerprint(request),
    )

    db.add(review)
    db.commit()

    return {
        "status": "pending",
        "message": "Review sent for moderation",
    }


@app.post("/api/v1/reports")
def submit_report(
    payload: ReportInput,
    request: Request,
    db: Session = Depends(get_db),
):
    check_write_mode(db)
    verify_turnstile(payload.turnstile_token)

    rate_limit(db, request, "report", 5, 60)

    phone = get_or_create_phone(db, payload.number)
    fp = fingerprint(request)

    
    existing = db.scalar(
        select(NumberReport).where(
            NumberReport.phone_id == phone.id,
            NumberReport.fingerprint == fp,
            NumberReport.created_at >= (
                utcnow() - timedelta(days=30)
            ),
        )
    )


    if existing:
        raise HTTPException(
            409,
            "A report was already submitted recently",
        )

    report = NumberReport(
        phone_id=phone.id,
        category=payload.category,
        body=payload.text.strip(),
        fingerprint=fp,
        status="pending",
    )

    db.add(report)
    db.commit()

    return {"status": "pending"}


@app.post("/api/v1/appeals")
def submit_appeal(
    payload: AppealInput,
    request: Request,
    db: Session = Depends(get_db),
):
    verify_turnstile(payload.turnstile_token)
    rate_limit(db, request, "appeal", 3, 60)

    e164, _ = normalize_number(payload.number)

    email = payload.contact_email

    db.add(Appeal(
        phone_e164=e164,
        review_id=payload.review_id,
        body=payload.text.strip(),
        contact_email=email,
        status="pending",
    ))

    db.commit()
    return {"status": "pending"}


# -----------------------
# Admin authentication
# -----------------------

@app.post("/api/v1/admin/login")
def admin_login(
    payload: LoginInput,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    rate_limit(db, request, "login", 5, 15)

    valid = False

    if payload.username == settings.admin_username:
        try:
            valid = hasher.verify(
                settings.admin_password_hash,
                payload.password,
            )
        except Exception:
            valid = False

    db.commit()

    if not valid:
        raise HTTPException(401, "Invalid credentials")

    token = secrets.token_urlsafe(48)

    db.add(AdminSession(
        token_hash=hashlib.sha256(
            token.encode()
        ).hexdigest(),
        expires_at=utcnow() + timedelta(hours=24),
    ))

    audit(db, "login", "admin", None)
    db.commit()

    response.set_cookie(
        COOKIE_NAME,
        token,
        httponly=True,
        secure=settings.cookie_secure,
        samesite="lax",
        max_age=86400,
        path="/",
    )

    return {"authenticated": True}


@app.get("/api/v1/admin/me")
def admin_me(
    _: bool = Depends(require_admin),
):
    return {"authenticated": True}


@app.post("/api/v1/admin/logout")
def admin_logout(
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
    _: bool = Depends(require_admin),
):
    token = request.cookies.get(COOKIE_NAME)

    if token:
        digest = hashlib.sha256(token.encode()).hexdigest()
        session = db.scalar(
            select(AdminSession).where(
                AdminSession.token_hash == digest
            )
        )

        if session:
            db.delete(session)
            db.commit()

    response.delete_cookie(COOKIE_NAME, path="/")

    return {"authenticated": False}


# -----------------------
# Admin dashboard
# -----------------------

@app.get("/api/v1/admin/dashboard")
def admin_dashboard(
    db: Session = Depends(get_db),
    _: bool = Depends(require_admin),
):
    def count(model, status=None):
        query = select(func.count(model.id))

        if status is not None:
            query = query.where(model.status == status)

        return db.scalar(query) or 0

    state = db.get(SystemState, 1)

    return {
        "phones": count(Phone),
        "reviews": count(Review),
        "pending_reviews": count(Review, "pending"),
        "reports": count(NumberReport),
        "pending_reports": count(NumberReport, "pending"),
        "pending_appeals": count(Appeal, "pending"),
        "mode": state.mode if state else "normal",
    }


# -----------------------
# Admin phone management
# -----------------------

def validate_business(name, source):
    if bool(name) != bool(source):
        raise HTTPException(
            422,
            "Business name and source URL must be set together",
        )

    if source and not source.startswith("https://"):
        raise HTTPException(
            422,
            "Source must use HTTPS",
        )


@app.get("/api/v1/admin/phones")
def admin_phones(
    q: str = "",
    db: Session = Depends(get_db),
    _: bool = Depends(require_admin),
):
    query = select(Phone).order_by(Phone.id.desc()).limit(100)

    if q.strip():
        query = (
            select(Phone)
            .where(Phone.e164.contains(q.strip()))
            .order_by(Phone.id.desc())
            .limit(100)
        )

    return [
        {
            "id": p.id,
            "number": p.e164,
            "business_name": p.business_name,
            "source_url": p.source_url,
            "is_listed": p.is_listed,
        }
        for p in db.scalars(query).all()
    ]


@app.post("/api/v1/admin/phones")
def admin_add_phone(
    payload: PhoneInput,
    db: Session = Depends(get_db),
    _: bool = Depends(require_admin),
):
    name = (payload.business_name or "").strip() or None
    source = (payload.source_url or "").strip() or None

    validate_business(name, source)

    phone = get_or_create_phone(db, payload.number)

    phone.business_name = name
    phone.source_url = source
    phone.is_listed = bool(name and source)

    audit(db, "upsert", "phone", phone.id)
    db.commit()

    return {"id": phone.id}


@app.patch("/api/v1/admin/phones/{phone_id}")
def admin_edit_phone(
    phone_id: int,
    payload: PhoneEdit,
    db: Session = Depends(get_db),
    _: bool = Depends(require_admin),
):
    phone = db.get(Phone, phone_id)

    if not phone:
        raise HTTPException(404, "Phone not found")

    name = (payload.business_name or "").strip() or None
    source = (payload.source_url or "").strip() or None

    validate_business(name, source)

    phone.business_name = name
    phone.source_url = source
    phone.is_listed = bool(name and source)

    audit(db, "update", "phone", phone.id)
    db.commit()

    return {"ok": True}


@app.delete("/api/v1/admin/phones/{phone_id}")
def admin_delete_phone(
    phone_id: int,
    db: Session = Depends(get_db),
    _: bool = Depends(require_admin),
):
    phone = db.get(Phone, phone_id)

    if not phone:
        raise HTTPException(404, "Phone not found")

    db.delete(phone)
    audit(db, "delete", "phone", phone_id)
    db.commit()

    return {"deleted": True}


# -----------------------
# Review moderation
# -----------------------

@app.get("/api/v1/admin/reviews")
def admin_reviews(
    status: str = "pending",
    db: Session = Depends(get_db),
    _: bool = Depends(require_admin),
):
    query = select(Review).order_by(
        Review.created_at.desc()
    ).limit(100)

    if status != "all":
        query = (
            select(Review)
            .where(Review.status == status)
            .order_by(Review.created_at.desc())
            .limit(100)
        )

    rows = db.scalars(query).all()

    return [
        {
            "id": r.id,
            "number": db.get(Phone, r.phone_id).e164,
            "rating": r.rating,
            "category": r.category,
            "text": r.body,
            "status": r.status,
            "risk_flags": r.risk_flags,
            "created_at": r.created_at,
        }
        for r in rows
    ]



@app.patch("/api/v1/admin/reviews/{review_id}")
def admin_moderate_review(
    review_id: int,
    payload: Decision,
    db: Session = Depends(get_db),
    _: bool = Depends(require_admin),
):
    return decide_pending(
        db,
        Review,
        review_id,
        payload.status,
        "review",
    )


@app.delete("/api/v1/admin/reviews/{review_id}")
def admin_delete_review(
    review_id: int,
    db: Session = Depends(get_db),
    _: bool = Depends(require_admin),
):
    review = db.get(Review, review_id)

    if not review:
        raise HTTPException(404, "Review not found")

    db.delete(review)
    audit(db, "delete", "review", review_id)
    db.commit()

    return {"deleted": True}


# -----------------------
# Report moderation
# -----------------------

@app.get("/api/v1/admin/reports")
def admin_reports(
    status: str = "pending",
    db: Session = Depends(get_db),
    _: bool = Depends(require_admin),
):
    query = select(NumberReport).order_by(
        NumberReport.created_at.desc()
    ).limit(100)

    if status != "all":
        query = (
            select(NumberReport)
            .where(NumberReport.status == status)
            .order_by(NumberReport.created_at.desc())
            .limit(100)
        )

    return [
        {
            "id": r.id,
            "number": db.get(Phone, r.phone_id).e164,
            "category": r.category,
            "text": r.body,
            "status": r.status,
        }
        for r in db.scalars(query).all()
    ]



@app.patch("/api/v1/admin/reports/{report_id}")
def admin_moderate_report(
    report_id: int,
    payload: Decision,
    db: Session = Depends(get_db),
    _: bool = Depends(require_admin),
):
    return decide_pending(
        db,
        NumberReport,
        report_id,
        payload.status,
        "report",
    )


@app.delete("/api/v1/admin/reports/{report_id}")
def admin_delete_report(
    report_id: int,
    db: Session = Depends(get_db),
    _: bool = Depends(require_admin),
):
    report = db.get(NumberReport, report_id)

    if not report:
        raise HTTPException(404, "Report not found")

    db.delete(report)
    audit(db, "delete", "report", report_id)
    db.commit()

    return {"deleted": True}


# -----------------------
# Appeals
# -----------------------

@app.get("/api/v1/admin/appeals")
def admin_appeals(
    db: Session = Depends(get_db),
    _: bool = Depends(require_admin),
):
    rows = db.scalars(
        select(Appeal)
        .order_by(Appeal.created_at.desc())
        .limit(100)
    ).all()

    return [
        {
            "id": a.id,
            "number": a.phone_e164,
            "review_id": a.review_id,
            "text": a.body,
            "contact_email": a.contact_email,
            "status": a.status,
        }
        for a in rows
    ]



@app.patch("/api/v1/admin/appeals/{appeal_id}")
def admin_handle_appeal(
    appeal_id: int,
    payload: AppealDecision,
    db: Session = Depends(get_db),
    _: bool = Depends(require_admin),
):
    return decide_pending(
        db,
        Appeal,
        appeal_id,
        payload.status,
        "appeal",
    )


@app.delete("/api/v1/admin/appeals/{appeal_id}")
def admin_delete_appeal(
    appeal_id: int,
    db: Session = Depends(get_db),
    _: bool = Depends(require_admin),
):
    appeal = db.get(Appeal, appeal_id)

    if not appeal:
        raise HTTPException(404, "Appeal not found")

    db.delete(appeal)
    audit(db, "delete", "appeal", appeal_id)
    db.commit()

    return {"deleted": True}


# -----------------------
# System administration
# -----------------------

@app.put("/api/v1/admin/maintenance")
def admin_set_maintenance(
    payload: MaintenanceInput,
    db: Session = Depends(get_db),
    _: bool = Depends(require_admin),
):
    state = db.get(SystemState, 1)

    if not state:
        state = SystemState(id=1, mode="normal")
        db.add(state)

    state.mode = payload.mode

    audit(db, "change_mode", "system", 1)
    db.commit()

    return {"mode": state.mode}


@app.get("/api/v1/admin/audit")
def admin_audit(
    db: Session = Depends(get_db),
    _: bool = Depends(require_admin),
):
    rows = db.scalars(
        select(AuditLog)
        .order_by(AuditLog.id.desc())
        .limit(100)
    ).all()

    return [
        {
            "id": a.id,
            "action": a.action,
            "target_type": a.target_type,
            "target_id": a.target_id,
            "created_at": a.created_at,
        }
        for a in rows
    ]