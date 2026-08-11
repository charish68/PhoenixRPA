"""add retries to workflow steps

Revision ID: 61f547bc8fa7
Revises: 87e6fd56b7c7
Create Date: 2026-08-08 13:17:33.958047
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "61f547bc8fa7"
down_revision: Union[str, Sequence[str], None] = "87e6fd56b7c7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "workflow_steps",
        sa.Column(
            "retries",
            sa.Integer(),
            nullable=False,
            server_default="0",
        ),
    )

    # Remove the database default after existing rows are populated
    op.alter_column(
        "workflow_steps",
        "retries",
        server_default=None,
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column(
        "workflow_steps",
        "retries",
    )