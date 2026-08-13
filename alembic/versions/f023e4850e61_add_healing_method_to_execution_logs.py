"""add healing method to execution logs

Revision ID: f023e4850e61
Revises: add_healing_metadata_001
Create Date: 2026-08-13
"""

from alembic import op
import sqlalchemy as sa


revision = "f023e4850e61"
down_revision = "add_healing_metadata_001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "execution_logs",
        sa.Column(
            "healing_method",
            sa.String(length=30),
            nullable=True,
        ),
    )


def downgrade() -> None:
    op.drop_column(
        "execution_logs",
        "healing_method",
    )