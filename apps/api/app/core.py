
from datetime import datetime, timezone

from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")

    database_url: str

    app_version: str
    proxy_shared_secret: str

    environment: str = "development"
    public_origin: str = "http://localhost:3000"
    cookie_secure: bool = False

    admin_username: str = "admin"
    admin_password_hash: str
    abuse_pepper: str
    turnstile_secret: str


settings = Settings()

if settings.environment == "production":
    if (
        not settings.cookie_secure
        or not settings.public_origin.startswith("https://")
        or not settings.admin_password_hash.startswith("$argon2id$")
        or settings.turnstile_secret.startswith("1x000000")
        or len(settings.abuse_pepper) < 32
        or len(settings.proxy_shared_secret) < 32
    ):
        raise RuntimeError("Unsafe production configuration")


def utcnow():
    return datetime.now(timezone.utc)


class Base(DeclarativeBase):
    pass


engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)


def get_db():
    with SessionLocal() as db:
        yield db
