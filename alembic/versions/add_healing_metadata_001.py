"""add healing metadata to execution logs

Revision ID: add_healing_metadata_001
Revises: 61039bac8819
Create Date: 2026-08-12
"""

from alembic import op
import sqlalchemy as sa


revision = "add_healing_metadata_001"
down_revision = "61039bac8819"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "execution_logs",
        sa.Column(
            "healing_status",
            sa.String(length=20),
            nullable=False,
            server_default="NONE",
        ),
    )

    op.add_column(
        "execution_logs",
        sa.Column(
            "original_selector",
            sa.String(),
            nullable=True,
        ),
    )

    op.add_column(
        "execution_logs",
        sa.Column(
            "healed_selector",
            sa.String(),
            nullable=True,
        ),
    )


def downgrade() -> None:
    op.drop_column(
        "execution_logs",
        "healed_selector",
    )

    op.drop_column(
        "execution_logs",
        "original_selector",
    )

    op.drop_column(
        "execution_logs",
        "healing_status",
    )
