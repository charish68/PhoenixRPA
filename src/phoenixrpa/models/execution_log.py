from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from phoenixrpa.db.base import Base


class ExecutionLog(Base):
    __tablename__ = "execution_logs"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    job_id: Mapped[int] = mapped_column(
        ForeignKey(
            "jobs.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    run_id: Mapped[int] = mapped_column(
        ForeignKey(
            "execution_runs.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    step_order: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    branch_path: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    action: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    healing_status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="NONE",
    )

    original_selector: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    healed_selector: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    started_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    finished_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    duration_ms: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    error_message: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    screenshot_path: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )
