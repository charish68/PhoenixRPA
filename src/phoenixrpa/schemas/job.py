from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class JobStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"


class JobCreate(BaseModel):
    name: str
    target_site: str


class JobResponse(BaseModel):
    id: int
    name: str
    target_site: str
    status: JobStatus
    created_at: datetime

    model_config = {
        "from_attributes": True
    }