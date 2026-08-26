from datetime import datetime
from enum import Enum

from pydantic import BaseModel, field_validator


class JobStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"


class JobCreate(BaseModel):
    name: str
    target_site: str

    @field_validator("name", "target_site")
    @classmethod
    def validate_required_text(
        cls,
        value: str,
    ) -> str:
        if not value.strip():
            raise ValueError(
                "Field cannot be empty."
            )

        return value.strip()


class JobResponse(BaseModel):
    id: int
    name: str
    target_site: str
    status: JobStatus
    created_at: datetime

    model_config = {
        "from_attributes": True
    }
