from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session

from phoenixrpa.db.dependency import get_db
from phoenixrpa.schemas.job import JobCreate
from phoenixrpa.services.job_service import JobService

router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"],
)


@router.post("/")
def create_job(
    payload: JobCreate,
    db: Session = Depends(get_db),
):
    service = JobService(db)

    return service.create_job(
        payload.name,
        payload.target_site,
    )


@router.get("/")
def list_jobs(
    db: Session = Depends(get_db),
):
    return JobService(db).list_jobs()


@router.get("/{job_id}")
def get_job(
    job_id: int = Path(gt=0),
    db: Session = Depends(get_db),
):
    job = JobService(db).get_job(job_id)

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found",
        )

    return job


@router.delete("/{job_id}")
def delete_job(
    job_id: int = Path(gt=0),
    db: Session = Depends(get_db),
):
    deleted = JobService(db).delete_job(job_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Job not found",
        )

    return {
        "message": "Job deleted successfully"
    }
