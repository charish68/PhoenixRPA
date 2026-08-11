from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from phoenixrpa.browser.manager import BrowserManager
from phoenixrpa.core.logger import logger
from phoenixrpa.db.dependency import get_db
from phoenixrpa.services.workflow_service import WorkflowService
from phoenixrpa.schemas.workflow import WorkflowStepCreate

router = APIRouter(
    prefix="/recorder",
    tags=["Recorder"],
)

# Single BrowserManager instance
browser = BrowserManager()


class RecorderEvent(BaseModel):
    action: str
    selector: str | None = None
    value: str | None = None
    path: str | None = None


# ============================================================
# START RECORDING
# ============================================================

@router.post("/start")
async def start_recording():
    """
    Start browser recorder.
    """

    logger.info("Starting recorder...")

    browser.recorder.start()

    await browser.start(
        headless=False,
    )

    logger.success("Recorder started")

    return {
        "message": "Recording started",
    }


# ============================================================
# RECEIVE RECORDER EVENT
# ============================================================

@router.post("/event")
async def record_event(event: RecorderEvent):
    """
    Receive events from Chrome extension.
    """

    if browser.recorder is None:
        logger.error("Recorder is not initialized")

        return {
            "message": "Recorder not initialized"
        }

    logger.info(
        f"Received Event -> "
        f"action={event.action}, "
        f"selector={event.selector}, "
        f"value={event.value}"
    )

    browser.recorder.record(
        action=event.action,
        selector=event.selector,
        value=event.value,
        path=event.path,
    )

    logger.success(
        f"Recorded action: {event.action}"
    )

    return {
        "message": "Recorded",
    }


# ============================================================
# STOP RECORDING + SAVE TO JOB
# ============================================================

@router.post("/stop")
async def stop_recording(
    job_id: int,
    db: Session = Depends(get_db),
):
    """
    Stop recording and save the recorded workflow to a job.
    """

    logger.info(
        f"Stopping recorder for Job #{job_id}..."
    )

    # --------------------------------------------------------
    # Stop accepting events
    # --------------------------------------------------------

    browser.recorder.stop()

    # --------------------------------------------------------
    # Convert recorded steps to workflow schema
    # --------------------------------------------------------

    steps = []

    for index, step in enumerate(
        browser.recorder.steps,
        start=1,
    ):
        steps.append(
            WorkflowStepCreate(
                step_order=index,
                action=step.action,
                selector=step.selector,
                value=browser.recorder._normalize_value(
                    step.value
                ),
                path=step.path,
                timeout=30000,
                retries=0,
            )
        )

    # --------------------------------------------------------
    # Save workflow to database
    # --------------------------------------------------------

    if steps:
        WorkflowService(db).create_steps(
            job_id,
            steps,
        )

        logger.success(
            f"Saved {len(steps)} workflow steps "
            f"to Job #{job_id}"
        )

    else:
        logger.warning(
            f"No workflow steps recorded for Job #{job_id}"
        )

    # --------------------------------------------------------
    # Keep JSON export for debugging/backup
    # --------------------------------------------------------

    browser.recorder.export(
        "recorded_workflow.json",
    )

    # --------------------------------------------------------
    # Close browser
    # --------------------------------------------------------

    await browser.close()

    logger.success(
        f"Workflow recording completed for Job #{job_id}"
    )

    return {
        "message": "Workflow saved successfully",
        "job_id": job_id,
        "steps": len(steps),
        "file": "recorded_workflow.json",
    }


# ============================================================
# GET CURRENT WORKFLOW
# ============================================================

@router.get("/workflow")
async def get_workflow():
    """
    Return currently recorded workflow.
    """

    return browser.recorder.steps
