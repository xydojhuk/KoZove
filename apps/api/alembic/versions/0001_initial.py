from alembic import op
import sqlalchemy as sa


revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "phone_numbers",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("e164", sa.String(20), nullable=False),
        sa.Column("country", sa.String(2), nullable=False),
        sa.Column("number_type", sa.String(32), nullable=False),
        sa.Column("business_name", sa.String(120)),
        sa.Column("source_url", sa.String(500)),
        sa.Column(
            "is_listed", sa.Boolean(),
            nullable=False, server_default=sa.false()
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )
    op.create_index(
        "ix_phone_numbers_e164",
        "phone_numbers",
        ["e164"],
        unique=True,
    )

    op.create_table(
        "reviews",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "phone_id",
            sa.Integer(),
            sa.ForeignKey("phone_numbers.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("rating", sa.Integer(), nullable=False),
        sa.Column("category", sa.String(40), nullable=False),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("status", sa.String(20), nullable=False),
        sa.Column("risk_flags", sa.JSON(), nullable=False),
        sa.Column("fingerprint", sa.String(64), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True)),
        sa.Column("moderated_at", sa.DateTime(timezone=True)),
        sa.CheckConstraint(
            "rating BETWEEN 1 AND 5", name="ck_review_rating"
        ),
    )
    op.create_index("ix_reviews_phone_id", "reviews", ["phone_id"])
    op.create_index("ix_reviews_status", "reviews", ["status"])

    op.create_table(
        "number_reports",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "phone_id",
            sa.Integer(),
            sa.ForeignKey("phone_numbers.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("category", sa.String(40), nullable=False),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("status", sa.String(20), nullable=False),
        sa.Column("fingerprint", sa.String(64), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True)),
        sa.Column("moderated_at", sa.DateTime(timezone=True)),
    )
    op.create_index(
        "ix_number_reports_phone_id",
        "number_reports",
        ["phone_id"],
    )
    op.create_index(
        "ix_number_reports_status",
        "number_reports",
        ["status"],
    )

    op.create_table(
        "appeals",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("phone_e164", sa.String(20), nullable=False),
        sa.Column("review_id", sa.Integer()),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("contact_email", sa.String(254)),
        sa.Column("status", sa.String(20), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True)),
    )
    op.create_index("ix_appeals_status", "appeals", ["status"])

    op.create_table(
        "admin_sessions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("token_hash", sa.String(64), nullable=False),
        sa.Column(
            "expires_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
    )
    op.create_index(
        "ix_admin_sessions_token_hash",
        "admin_sessions",
        ["token_hash"],
        unique=True,
    )

    op.create_table(
        "audit_logs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("action", sa.String(60), nullable=False),
        sa.Column("target_type", sa.String(40), nullable=False),
        sa.Column("target_id", sa.Integer()),
        sa.Column("created_at", sa.DateTime(timezone=True)),
    )

    op.create_table(
        "abuse_events",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("fingerprint", sa.String(64), nullable=False),
        sa.Column("action", sa.String(30), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True)),
    )
    op.create_index(
        "ix_abuse_lookup",
        "abuse_events",
        ["fingerprint", "action", "created_at"],
    )

    op.create_table(
        "system_state",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("mode", sa.String(20), nullable=False),
    )
    op.execute(
        "INSERT INTO system_state (id, mode) "
        "VALUES (1, 'normal')"
    )


def downgrade():
    op.drop_table("system_state")
    op.drop_table("abuse_events")
    op.drop_table("audit_logs")
    op.drop_table("admin_sessions")
    op.drop_table("appeals")
    op.drop_table("number_reports")
    op.drop_table("reviews")
    op.drop_table("phone_numbers")