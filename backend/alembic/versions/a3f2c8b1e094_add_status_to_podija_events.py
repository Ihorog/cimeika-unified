"""Add status to podija_events

Revision ID: a3f2c8b1e094
Revises: 777d0bc4fdf7
Create Date: 2026-02-21 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "a3f2c8b1e094"
down_revision = "777d0bc4fdf7"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "podija_events",
        sa.Column("status", sa.String(), nullable=False, server_default="planned"),
    )


def downgrade() -> None:
    op.drop_column("podija_events", "status")
