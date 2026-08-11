"""add execution runs

Revision ID: e01695819398
Revises: d10a945d434c
Create Date: 2026-08-11 14:11:03.968329
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "e01695819398"
down_revision: Union[str, Sequence[str], None] = "d10a945d434c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # --------------------------------------------------
    # 1. Create execution_runs
    # --------------------------------------------------

    op.create_table(
        "execution_runs",
        sa.Column(
            "id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "job_id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "status",
            sa.String(length=20),
            nullable=False,
        ),
        sa.Column(
            "started_at",
            sa.DateTime(),
            nullable=False,
        ),
        sa.Column(
            "finished_at",
            sa.DateTime(),
            nullable=True,
        ),
        sa.Column(
            "duration_ms",
            sa.Integer(),
            nullable=True,
        ),
        sa.Column(
            "error_message",
            sa.String(),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["job_id"],
            ["jobs.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_execution_runs_job_id",
        "execution_runs",
        ["job_id"],
        unique=False,
    )

    # --------------------------------------------------
    # 2. Add run_id temporarily as nullable
    # --------------------------------------------------

    op.add_column(
        "execution_logs",
        sa.Column(
            "run_id",
            sa.Integer(),
            nullable=True,
        ),
    )

    # --------------------------------------------------
    # 3. Create one legacy run for each existing job
    #
    # Existing execution logs pre-date execution_runs.
    # We preserve them by placing them into a legacy run.
    # --------------------------------------------------

    connection = op.get_bind()

    connection.execute(
        sa.text(
            """
            INSERT INTO execution_runs (
                job_id,
                status,
                started_at,
                finished_at,
                duration_ms,
                error_message
            )
            SELECT
                job_id,
                CASE
                    WHEN BOOL_OR(status = 'FAILED')
                        THEN 'FAILED'
                    ELSE 'SUCCESS'
                END AS status,
                MIN(started_at) AS started_at,
                MAX(finished_at) AS finished_at,
                SUM(duration_ms) AS duration_ms,
                MAX(error_message) AS error_message
            FROM execution_logs
            GROUP BY job_id
            """
        )
    )

    # --------------------------------------------------
    # 4. Assign old execution logs to their legacy run
    # --------------------------------------------------

    connection.execute(
        sa.text(
            """
            UPDATE execution_logs AS logs
            SET run_id = runs.id
            FROM execution_runs AS runs
            WHERE logs.job_id = runs.job_id
              AND logs.run_id IS NULL
            """
        )
    )

    # --------------------------------------------------
    # 5. Make run_id mandatory
    # --------------------------------------------------

    op.alter_column(
        "execution_logs",
        "run_id",
        existing_type=sa.Integer(),
        nullable=False,
    )

    # --------------------------------------------------
    # 6. Add foreign key
    # --------------------------------------------------

    op.create_foreign_key(
        "fk_execution_logs_run_id",
        "execution_logs",
        "execution_runs",
        ["run_id"],
        ["id"],
        ondelete="CASCADE",
    )

    # --------------------------------------------------
    # 7. Add index
    # --------------------------------------------------

    op.create_index(
        "ix_execution_logs_run_id",
        "execution_logs",
        ["run_id"],
        unique=False,
    )


def downgrade() -> None:

    op.drop_index(
        "ix_execution_logs_run_id",
        table_name="execution_logs",
    )

    op.drop_constraint(
        "fk_execution_logs_run_id",
        "execution_logs",
        type_="foreignkey",
    )

    op.drop_column(
        "execution_logs",
        "run_id",
    )

    op.drop_index(
        "ix_execution_runs_job_id",
        table_name="execution_runs",
    )

    op.drop_table(
        "execution_runs",
    )