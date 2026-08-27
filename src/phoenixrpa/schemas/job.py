from datetime import datetime
from enum import Enum
from typing import Annotated

from pydantic import BaseModel, StringConstraints


class JobStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"


NonEmptyJobName = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=1,
        max_length=255,
    ),
]

NonEmptyTargetSite = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=1,
        max_length=2048,
    ),
]


class JobCreate(BaseModel):
    name: NonEmptyJobName
    target_site: NonEmptyTargetSite


class JobResponse(BaseModel):
    id: int
    name: str
    target_site: str
    status: JobStatus
    created_at: datetime

    model_config = {
        "from_attributes": True
    }
