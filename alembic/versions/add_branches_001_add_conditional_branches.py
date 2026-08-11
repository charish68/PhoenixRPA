"""add conditional branches to workflow steps

Revision ID: add_branches_001
Revises: add_condition_001
Create Date: 2026-08-11
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "add_branches_001"
down_revision: Union[str, Sequence[str], None] = "add_condition_001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "workflow_steps",
        sa.Column(
            "parent_step_id",
            sa.Integer(),
            nullable=True,
        ),
    )

    op.add_column(
        "workflow_steps",
        sa.Column(
            "branch",
            sa.String(length=10),
            nullable=True,
        ),
    )

    op.create_foreign_key(
        "fk_workflow_steps_parent_step",
        "workflow_steps",
        "workflow_steps",
        ["parent_step_id"],
        ["id"],
        ondelete="CASCADE",
    )

    op.create_index(
        "ix_workflow_steps_parent_step_id",
        "workflow_steps",
        ["parent_step_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_workflow_steps_parent_step_id",
        table_name="workflow_steps",
    )

    op.drop_constraint(
        "fk_workflow_steps_parent_step",
        "workflow_steps",
        type_="foreignkey",
    )

    op.drop_column(
        "workflow_steps",
        "branch",
    )

    op.drop_column(
        "workflow_steps",
        "parent_step_id",
    )
