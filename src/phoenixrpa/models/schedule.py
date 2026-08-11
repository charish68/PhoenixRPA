from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from phoenixrpa.db.base import Base


class Schedule(Base):
    __tablename__ = "schedules"

    id: Mapped[int] = mapped_column(primary_key=True)

    job_id: Mapped[int] = mapped_column(
        ForeignKey("jobs.id")
    )

    cron: Mapped[str]

    enabled: Mapped[bool] = mapped_column(
        default=True,
    )

    created_at: Mapped[datetime]