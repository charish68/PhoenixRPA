from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from phoenixrpa.db.base import Base


class WorkflowStep(Base):
    __tablename__ = "workflow_steps"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    job_id: Mapped[int] = mapped_column(
        ForeignKey(
            "jobs.id",
            ondelete="CASCADE",
        )
    )

    step_order: Mapped[int] = mapped_column(
        Integer
    )

    action: Mapped[str] = mapped_column(
        String(50)
    )

    selector: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    value: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    path: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    timeout: Mapped[int] = mapped_column(
        Integer,
        default=30000,
    )

    retries: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    condition: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    parent_step_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            "workflow_steps.id",
            ondelete="CASCADE",
        ),
        nullable=True,
    )

    branch: Mapped[str | None] = mapped_column(
        String(10),
        nullable=True,
    )

    job = relationship(
        "Job",
        back_populates="steps",
    )

    parent = relationship(
        "WorkflowStep",
        remote_side=[id],
        back_populates="children",
    )

    children = relationship(
        "WorkflowStep",
        back_populates="parent",
        cascade="all, delete-orphan",
    )
