from pathlib import Path

from sqlalchemy.orm import Session
from loguru import logger

from phoenixrpa.browser.manager import BrowserManager
from phoenixrpa.services.execution_service import ExecutionService
from phoenixrpa.workflow.dispatcher import WorkflowDispatcher
from phoenixrpa.workflow.models import Workflow, WorkflowStep
from phoenixrpa.workflow.variables import VariableResolver


class WorkflowRunner:

    def __init__(
        self,
        browser: BrowserManager,
        variables: dict[str, str] | None = None,
        db: Session | None = None,
        run_id: int | None = None,
    ):
        self.browser = browser

        self.variables = VariableResolver(
            variables or {}
        )

        if db is None:
            raise ValueError(
                "WorkflowRunner requires a database session"
            )

        self.run_id = run_id

        self.execution_service = ExecutionService(
            db
        )

        self.dispatcher = WorkflowDispatcher(
            browser,
            self.variables,
            db,
        )

    async def run_step(
        self,
        step: WorkflowStep,
        log_execution: bool = False,
        branch_path: str | None = None,
    ):
        """
        Execute a workflow step with retry support.
        """

        # Preserve the selector before variable resolution.
        original_selector = step.selector
        original_value = step.value
        original_path = step.path

        step.selector = self.variables.resolve(
            step.selector
        )

        step.value = self.variables.resolve(
            step.value
        )

        step.path = self.variables.resolve(
            step.path
        )

        retries = step.retries or 0

        log = None

        # --------------------------------------------------
        # Create execution log for this step
        # --------------------------------------------------

        if (
            log_execution
            and self.run_id is not None
            and step.job_id is not None
        ):
            log = self.execution_service.start_step(
                job_id=step.job_id,
                step_order=step.step_order,
                action=step.action,
                run_id=self.run_id,
                branch_path=branch_path,
                original_selector=original_selector,
            )

        # --------------------------------------------------
        # Execute with retry support
        # --------------------------------------------------

        for attempt in range(retries + 1):

            try:

                logger.info(
                    f"Executing step '{step.action}' "
                    f"(Attempt {attempt + 1}/{retries + 1})"
                )

                healing_info = await self.dispatcher.dispatch(
                    step,
                    execute_child=self._execute_nested_step,
                    branch_path=branch_path,
                )

                # --------------------------------------------------
                # Record selector healing metadata
                # --------------------------------------------------

                if (
                    log is not None
                    and healing_info is not None
                    and healing_info.get("status") == "HEALED"
                ):
                    self.execution_service.mark_step_healed(
                        log,
                        healing_info["original_selector"],
                        healing_info["healed_selector"],
                        healing_method=healing_info.get("method"),
                        healing_confidence=healing_info.get("confidence"),
                    )

                # --------------------------------------------------
                # Step succeeded
                # --------------------------------------------------

                if log is not None:
                    self.execution_service.finish_step(
                        log
                    )

                logger.success(
                    f"Step '{step.action}' "
                    f"completed successfully"
                )

                step.selector = original_selector
                step.value = original_value
                step.path = original_path

                return

            except Exception as e:

                logger.warning(
                    f"Step '{step.action}' failed "
                    f"(Attempt {attempt + 1}/{retries + 1})"
                )

                # --------------------------------------------------
                # Retry
                # --------------------------------------------------

                if attempt < retries:
                    continue

                # --------------------------------------------------
                # Final failure
                # --------------------------------------------------

                if log is not None:

                    # --------------------------------------------------
                    # An IF can receive an exception from a child.
                    # The child owns the failure.
                    # --------------------------------------------------

                    if step.action.strip().lower() != "if":

                        screenshot_path = None

                        if self.run_id is not None:
                            try:

                                job_id = step.job_id

                                screenshot_path = (
                                    Path("recorded")
                                    / "failures"
                                    / (
                                        f"job_{job_id}_"
                                        f"run_{self.run_id}_"
                                        f"step_{step.step_order}_"
                                        f"failure.png"
                                    )
                                )

                                screenshot_path.parent.mkdir(
                                    parents=True,
                                    exist_ok=True,
                                )

                                logger.info(
                                    "Capturing step failure screenshot: "
                                    f"{screenshot_path}"
                                )

                                await self.browser.screenshots.capture_page(
                                    str(screenshot_path)
                                )

                                log.screenshot_path = (
                                    screenshot_path.as_posix()
                                )

                                logger.success(
                                    "Step failure screenshot saved: "
                                    f"{screenshot_path}"
                                )

                            except Exception as screenshot_error:

                                logger.exception(
                                    "Failed to capture step failure "
                                    f"screenshot: {screenshot_error}"
                                )

                                log.screenshot_path = None

                        self.execution_service.fail_step(
                            log,
                            str(e),
                        )

                    else:

                        # --------------------------------------------------
                        # Child failed inside IF.
                        # The IF condition itself was evaluated successfully.
                        # --------------------------------------------------

                        self.execution_service.finish_step(
                            log
                        )

                        logger.warning(
                            f"Child step failed inside IF "
                            f"(step {step.step_order}); "
                            f"keeping IF execution successful"
                        )

                logger.exception(e)

                # --------------------------------------------------
                # Propagate the actual child failure.
                # --------------------------------------------------

                step.selector = original_selector
                step.value = original_value
                step.path = original_path

                raise


    async def _execute_nested_step(
        self,
        step: WorkflowStep,
        branch_path: str | None = None,
    ):
        """
        Execute a conditional branch child and record
        its branch path.
        """

        await self.run_step(
            step,
            log_execution=True,
            branch_path=branch_path,
        )

    async def run(
        self,
        workflow: Workflow,
    ):
        """
        Execute an entire workflow.
        """

        logger.info(
            f"Starting workflow with "
            f"{len(workflow.steps)} step(s)"
        )

        for step in workflow.steps:

            await self.run_step(
            step,
            log_execution=True,
        )

        logger.success(
            "Workflow execution completed"
        )






