from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from phoenixrpa.db.dependency import get_db
from phoenixrpa.repositories.job_repository import JobRepository
from phoenixrpa.workflow.validator import WorkflowValidationError
from phoenixrpa.workers.job_executor import JobExecutor


router = APIRouter(
    prefix="/execute",
    tags=["Execution"],
)


class ExecuteRequest(BaseModel):
    variables: dict[str, str] = {}


@router.post("/{job_id}")
async def execute_job(
    job_id: int,
    payload: ExecuteRequest | None = None,
    db: Session = Depends(get_db),
):
    # --------------------------------------------------
    # Get job
    # --------------------------------------------------

    repo = JobRepository(db)

    job = repo.get(job_id)

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found",
        )

    # --------------------------------------------------
    # Execute job
    # --------------------------------------------------

    executor = JobExecutor(db)

    try:
        await executor.execute(
            job,
            variables=payload.variables if payload else None,
        )

    except WorkflowValidationError as e:

        raise HTTPException(
            status_code=400,
            detail=f"Workflow validation failed: {str(e)}",
        ) from e

    except Exception as e:

        raise HTTPException(
            status_code=422,
            detail={
                "message": "Job execution failed",
                "error": str(e),
                "job_id": job_id,
            },
        ) from e

    # --------------------------------------------------
    # Success
    # --------------------------------------------------

    return {
        "message": "Job completed",
        "job_id": job_id,
        "status": "COMPLETED",
    }
