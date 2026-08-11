"""add condition to workflow steps

Revision ID: add_condition_001
Revises: 61f547bc8fa7
Create Date: 2026-08-11
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "add_condition_001"
down_revision: Union[str, Sequence[str], None] = "e01695819398"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "workflow_steps",
        sa.Column(
            "condition",
            sa.String(),
            nullable=True,
        ),
    )


def downgrade() -> None:
    op.drop_column(
        "workflow_steps",
        "condition",
    )
