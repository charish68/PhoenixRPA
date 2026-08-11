from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from phoenixrpa.db.dependency import get_db
from phoenixrpa.schemas.workflow import WorkflowStepCreate
from phoenixrpa.services.workflow_service import WorkflowService

router = APIRouter(
    prefix="/jobs/{job_id}/steps",
    tags=["Workflow"],
)


@router.post("/")
def create_steps(
    job_id: int,
    payload: list[WorkflowStepCreate],
    db: Session = Depends(get_db),
):
    WorkflowService(db).create_steps(job_id, payload)

    return {
        "message": "Workflow created successfully"
    }


@router.get("/")
def get_steps(
    job_id: int,
    db: Session = Depends(get_db),
):
    return WorkflowService(db).get_steps(job_id)