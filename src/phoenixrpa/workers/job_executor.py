from pathlib import Path

from loguru import logger

from phoenixrpa.browser.manager import BrowserManager
from phoenixrpa.models.job import JobStatus
from phoenixrpa.repositories.job_repository import JobRepository
from phoenixrpa.repositories.workflow_repository import WorkflowRepository
from phoenixrpa.services.execution_service import ExecutionService
from phoenixrpa.workflow.models import Workflow, WorkflowStep
from phoenixrpa.workflow.runner import WorkflowRunner
from phoenixrpa.workflow.validator import WorkflowValidationError


class JobExecutor:

    def __init__(self, db):
        self.db = db
        self.job_repo = JobRepository(db)
        self.workflow_repo = WorkflowRepository(db)
        self.execution_service = ExecutionService(db)

    async def execute(
        self,
        job,
        variables: dict[str, str] | None = None,
    ):
        logger.info(
            f"Executing Job #{job.id}"
        )

        self.job_repo.update_status(
            job.id,
            JobStatus.RUNNING,
        )

        browser = BrowserManager()

        run = self.execution_service.start_run(
            job.id,
        )

        logger.info(
            f"Created execution run #{run.id} "
            f"for job #{job.id}"
        )

        try:
            logger.info(
                f"Loading workflow for job #{job.id}"
            )

            db_steps = self.workflow_repo.get_steps(
                job.id
            )

            if not db_steps:
                raise ValueError(
                    f"No workflow steps found for job {job.id}"
                )

            logger.info(
                f"Loaded {len(db_steps)} workflow step(s)"
            )

            def build_step(db_step):
                workflow_step = WorkflowStep(
                    job_id=db_step.job_id,
                    step_order=db_step.step_order,
                    action=db_step.action,
                    selector=db_step.selector,
                    value=db_step.value,
                    path=db_step.path,
                    timeout=db_step.timeout,
                    retries=db_step.retries,
                    condition=db_step.condition,
                )

                children = [
                    child
                    for child in db_steps
                    if child.parent_step_id == db_step.id
                ]

                for child in children:
                    child_step = build_step(child)

                    if child.branch == "true":
                        workflow_step.true_steps.append(
                            child_step
                        )

                    elif child.branch == "false":
                        workflow_step.false_steps.append(
                            child_step
                        )

                return workflow_step

            root_steps = [
                build_step(step)
                for step in db_steps
                if step.parent_step_id is None
            ]

            workflow = Workflow(
                steps=root_steps
            )

            logger.info(
                "Workflow converted successfully"
            )

            logger.info(
                f"Validating workflow for job #{job.id}"
            )

            from phoenixrpa.workflow.validator import WorkflowValidator

            validator = WorkflowValidator()

            validator.validate(
                workflow
            )

            logger.success(
                "Workflow validation passed"
            )

            logger.info(
                "Starting browser for job execution..."
            )

            await browser.start(
                headless=False,
            )

            logger.success(
                "Browser started for job execution"
            )

            if not job.target_site:
                raise ValueError(
                    f"Job #{job.id} has no target_site"
                )

            logger.info(
                f"Navigating to target site: "
                f"{job.target_site}"
            )

            await browser.page.goto(
                job.target_site,
                wait_until="domcontentloaded",
            )

            logger.success(
                f"Navigated to: {job.target_site}"
            )

            runner = WorkflowRunner(
                browser=browser,
                variables=variables,
                db=self.db,
                run_id=run.id,
            )

            # --------------------------------------------------
            # WorkflowRunner owns individual step execution logs.
            # This is important because selector healing metadata
            # is recorded by WorkflowRunner.
            # --------------------------------------------------

            for index, step in enumerate(
                workflow.steps,
                start=1,
            ):
                logger.info(
                    f"Starting step {index}/"
                    f"{len(workflow.steps)}: "
                    f"{step.action}"
                )

                await runner.run_step(
                    step,
                    log_execution=True,
                )

                logger.success(
                    f"Step {index} completed: "
                    f"{step.action}"
                )

            self.execution_service.finish_run(
                run
            )

            self.job_repo.update_status(
                job.id,
                JobStatus.SUCCESS,
            )

            logger.success(
                f"Execution run #{run.id} completed successfully"
            )

            logger.success(
                f"Job #{job.id} completed successfully"
            )

        except WorkflowValidationError as e:

            self.execution_service.fail_run(
                run,
                str(e),
            )

            self.job_repo.update_status(
                job.id,
                JobStatus.FAILED,
            )

            logger.error(
                f"Workflow validation failed for "
                f"job #{job.id}: {e}"
            )

            raise

        except Exception as e:

            logger.exception(
                f"Job #{job.id} failed: {e}"
            )

            self.execution_service.fail_run(
                run,
                str(e),
            )

            self.job_repo.update_status(
                job.id,
                JobStatus.FAILED,
            )

            raise

        finally:

            logger.info(
                f"Closing browser for job #{job.id}"
            )

            await browser.close()

            logger.info(
                f"Browser closed for job #{job.id}"
            )
