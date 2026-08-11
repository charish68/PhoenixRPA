from sqlalchemy.orm import Session

from phoenixrpa.models.workflow_step import WorkflowStep
from phoenixrpa.schemas.workflow import WorkflowStepCreate


class WorkflowRepository:

    def __init__(self, db: Session):
        self.db = db

    def create_steps(
        self,
        job_id: int,
        steps: list[WorkflowStepCreate],
    ):
        db_steps = []

        def create_step(
            step: WorkflowStepCreate,
            parent_step_id: int | None = None,
            branch: str | None = None,
        ):
            db_step = WorkflowStep(
                job_id=job_id,
                step_order=step.step_order,
                action=step.action,
                selector=step.selector,
                value=step.value,
                path=step.path,
                timeout=step.timeout,
                retries=step.retries,
                condition=step.condition,
                parent_step_id=parent_step_id,
                branch=branch,
            )

            self.db.add(db_step)
            self.db.flush()

            db_steps.append(db_step)

            for child in step.true_steps:
                create_step(
                    child,
                    parent_step_id=db_step.id,
                    branch="true",
                )

            for child in step.false_steps:
                create_step(
                    child,
                    parent_step_id=db_step.id,
                    branch="false",
                )

        for step in steps:
            create_step(step)

        self.db.commit()

        for step in db_steps:
            self.db.refresh(step)

        return db_steps

    def get_steps(
        self,
        job_id: int,
    ):
        return (
            self.db.query(WorkflowStep)
            .filter(WorkflowStep.job_id == job_id)
            .order_by(WorkflowStep.step_order)
            .all()
        )

    def update_selector(
        self,
        job_id: int,
        step_order: int,
        selector: str,
    ):
        step = (
            self.db.query(WorkflowStep)
            .filter(
                WorkflowStep.job_id == job_id,
                WorkflowStep.step_order == step_order,
            )
            .first()
        )

        if step is None:
            return False

        step.selector = selector
        self.db.commit()

        return True

    def delete_steps(
        self,
        job_id: int,
    ):
        self.db.query(WorkflowStep).filter(
            WorkflowStep.job_id == job_id
        ).delete()

        self.db.commit()
