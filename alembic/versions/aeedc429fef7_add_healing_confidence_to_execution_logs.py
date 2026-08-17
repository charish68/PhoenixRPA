"""add healing confidence to execution logs

Revision ID: aeedc429fef7
Revises: f023e4850e61
Create Date: 2026-08-13 17:08:03.257893

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'aeedc429fef7'
down_revision: Union[str, Sequence[str], None] = 'f023e4850e61'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
