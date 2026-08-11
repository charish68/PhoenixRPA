from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from phoenixrpa.db.dependency import get_db
from phoenixrpa.models.execution_log import ExecutionLog
from phoenixrpa.services.execution_service import ExecutionService


router = APIRouter(
    prefix="/jobs/{job_id}",
    tags=["Execution History"],
)


# ==================================================
# All execution runs for a job
# ==================================================

@router.get("/runs")
def get_execution_runs(
    job_id: int,
    db: Session = Depends(get_db),
):
    return ExecutionService(db).list_runs(job_id)


# ==================================================
# Logs for one execution run
# ==================================================

@router.get("/runs/{run_id}/logs")
def get_run_logs(
    job_id: int,
    run_id: int,
    db: Session = Depends(get_db),
):
    service = ExecutionService(db)

    runs = service.list_runs(job_id)

    run = next(
        (
            item
            for item in runs
            if item.id == run_id
        ),
        None,
    )

    if run is None:
        raise HTTPException(
            status_code=404,
            detail="Execution run not found",
        )

    return service.list_run_logs(run_id)


# ==================================================
# Legacy endpoint
#
# Keeps the existing dashboard/API working.
# ==================================================

@router.get("/executions/")
def get_execution_logs(
    job_id: int,
    db: Session = Depends(get_db),
):
    return ExecutionService(db).list_logs(job_id)


# ==================================================
# Screenshot for an execution step
# ==================================================

@router.get(
    "/executions/{execution_id}/screenshot"
)
def get_execution_screenshot(
    job_id: int,
    execution_id: int,
    db: Session = Depends(get_db),
):

    # --------------------------------------------------
    # Find execution log
    # --------------------------------------------------

    log = (
        db.query(ExecutionLog)
        .filter(
            ExecutionLog.id == execution_id,
            ExecutionLog.job_id == job_id,
        )
        .first()
    )

    if log is None:
        raise HTTPException(
            status_code=404,
            detail="Execution log not found",
        )

    # --------------------------------------------------
    # Check screenshot path
    # --------------------------------------------------

    if not log.screenshot_path:
        raise HTTPException(
            status_code=404,
            detail="No screenshot available for this execution",
        )

    # --------------------------------------------------
    # Resolve screenshot path
    # --------------------------------------------------

    screenshot_path = Path(
        log.screenshot_path
    )

    if not screenshot_path.is_absolute():
        screenshot_path = (
            Path.cwd() / screenshot_path
        )

    screenshot_path = screenshot_path.resolve()

    # --------------------------------------------------
    # Check file exists
    # --------------------------------------------------

    if not screenshot_path.is_file():
        raise HTTPException(
            status_code=404,
            detail="Screenshot file not found",
        )

    # --------------------------------------------------
    # Return screenshot
    # --------------------------------------------------

    return FileResponse(
        path=str(screenshot_path),
        media_type="image/png",
        filename=screenshot_path.name,
    )
