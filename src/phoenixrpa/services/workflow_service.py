from sqlalchemy.orm import Session

from phoenixrpa.repositories.workflow_repository import WorkflowRepository
from phoenixrpa.schemas.workflow import WorkflowStepCreate


class WorkflowService:
    def __init__(self, db: Session):
        self.repo = WorkflowRepository(db)

    def create_steps(
        self,
        job_id: int,
        payload: list[WorkflowStepCreate],
    ):
        # Replace existing workflow for this job
        self.repo.delete_steps(job_id)

        return self.repo.create_steps(
            job_id,
            payload,
        )

    def get_steps(
        self,
        job_id: int,
    ):
        return self.repo.get_steps(job_id)

    def update_selector(
        self,
        job_id: int,
        step_order: int,
        selector: str,
    ):
        return self.repo.update_selector(
            job_id,
            step_order,
            selector,
        )
