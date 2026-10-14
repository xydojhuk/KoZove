
import os
import uuid

import pytest

from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url
from sqlalchemy.orm import sessionmaker


os.environ.setdefault(
    "DATABASE_URL",
    "postgresql+psycopg://test:test@127.0.0.1:5432/kozove_test",
)
os.environ.setdefault("APP_VERSION", "0.1.3")
os.environ.setdefault(
    "ADMIN_PASSWORD_HASH",
    "not-used-in-tests",
)
os.environ.setdefault(
    "ABUSE_PEPPER",
    "a-test-pepper-not-for-real-data-123456789",
)
os.environ.setdefault(
    "PROXY_SHARED_SECRET",
    "a-test-proxy-secret-not-for-production",
)
os.environ.setdefault(
    "TURNSTILE_SECRET",
    "1x0000000000000000000000000000000AA",
)

from app.core import Base
import app.models


@pytest.fixture()
def pg_session_factory():
    url = os.getenv("KOZOVE_TEST_DATABASE_URL")

    if not url:
        pytest.skip(
            "Set KOZOVE_TEST_DATABASE_URL "
            "to a disposable PostgreSQL test database"
        )

    parsed = make_url(url)

    if (
        parsed.get_backend_name() != "postgresql"
        or "test" not in (parsed.database or "").lower()
    ):
        pytest.fail(
            "Refusing to use a database "
            "without 'test' in its name"
        )

    schema = "kozove_" + uuid.uuid4().hex

    admin_engine = create_engine(url)

    with admin_engine.begin() as conn:
        conn.execute(
            text(f'CREATE SCHEMA "{schema}"')
        )

    engine = create_engine(
        url,
        connect_args={
            "options": f"-csearch_path={schema},public"
        },
    )

    try:
        Base.metadata.create_all(engine)

        yield sessionmaker(
            bind=engine,
            expire_on_commit=False,
        )
    finally:
        engine.dispose()

        with admin_engine.begin() as conn:
            conn.execute(
                text(
                    f'DROP SCHEMA "{schema}" CASCADE'
                )
            )

        admin_engine.dispose()
