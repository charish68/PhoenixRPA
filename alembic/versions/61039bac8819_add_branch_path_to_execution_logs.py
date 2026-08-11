"""add branch path to execution logs

Revision ID: 61039bac8819
Revises: add_branches_001
Create Date: 2026-08-11
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "61039bac8819"
down_revision = "add_branches_001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "execution_logs",
        sa.Column(
            "branch_path",
            sa.String(length=255),
            nullable=True,
        ),
    )


def downgrade() -> None:
    op.drop_column(
        "execution_logs",
        "branch_path",
    )
