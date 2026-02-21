"""Add reminder_jobs table

Revision ID: b1c2d3e4f5a6
Revises: 777d0bc4fdf7
Create Date: 2026-02-21 10:00:00.000000

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "b1c2d3e4f5a6"
down_revision = "777d0bc4fdf7"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')

    op.create_table(
        "reminder_jobs",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("uuid_generate_v4()"),
            nullable=False,
        ),
        sa.Column("event_id", sa.Integer(), nullable=False),
        sa.Column(
            "user_id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column("remind_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("channel", sa.String(length=64), nullable=False, server_default="telegram"),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="pending"),
        sa.Column("attempts", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("last_error", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["event_id"], ["podija_events.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index("idx_reminder_jobs_event_id", "reminder_jobs", ["event_id"])
    op.create_index("idx_reminder_jobs_user_id", "reminder_jobs", ["user_id"])
    op.create_index("idx_reminder_jobs_remind_at", "reminder_jobs", ["remind_at"])
    op.create_index("idx_reminder_jobs_status", "reminder_jobs", ["status"])

    op.execute(
        "CREATE TRIGGER update_reminder_jobs_updated_at "
        "BEFORE UPDATE ON reminder_jobs "
        "FOR EACH ROW EXECUTE FUNCTION update_updated_at_column()"
    )


def downgrade() -> None:
    op.execute(
        "DROP TRIGGER IF EXISTS update_reminder_jobs_updated_at ON reminder_jobs"
    )
    op.drop_index("idx_reminder_jobs_status", table_name="reminder_jobs")
    op.drop_index("idx_reminder_jobs_remind_at", table_name="reminder_jobs")
    op.drop_index("idx_reminder_jobs_user_id", table_name="reminder_jobs")
    op.drop_index("idx_reminder_jobs_event_id", table_name="reminder_jobs")
    op.drop_table("reminder_jobs")
