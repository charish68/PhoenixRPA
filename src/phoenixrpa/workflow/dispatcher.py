from sqlalchemy.orm import Session

from phoenixrpa.browser.manager import BrowserManager
from phoenixrpa.core.logger import logger
from phoenixrpa.services.workflow_service import WorkflowService
from phoenixrpa.workflow.condition import ConditionEvaluator
from phoenixrpa.workflow.models import WorkflowStep
from phoenixrpa.workflow.variables import VariableResolver


class WorkflowDispatcher:

    def __init__(
        self,
        browser: BrowserManager,
        variables: VariableResolver,
        db: Session,
    ):
        self.browser = browser
        self.variables = variables
        self.condition_evaluator = ConditionEvaluator()
        self.workflow_service = WorkflowService(db)

    async def _execute_with_healing(
        self,
        step: WorkflowStep,
        action,
    ):
        """
        Execute a browser action with automatic selector healing.

        Returns:
            None when the original selector succeeds.
            A healing metadata dictionary when a selector is healed.
        """

        original_selector = step.selector

        try:
            await action(step.selector)

            return None

        except Exception:
            logger.warning(
                f"Selector '{step.selector}' failed. "
                "Attempting healing..."
            )

            healing_result = (
                await self.browser.healer.find_best_selector(
                    step.selector,
                    return_result=True,
                )
            )

            if healing_result is None:
                raise

            healed = healing_result.healed_selector

            if healed is None:
                raise RuntimeError(
                    "Healing returned a result without "
                    "a healed selector."
                )

            logger.success(
                f"Selector healed: "
                f"{step.selector} -> {healed} "
                f"(method={healing_result.method})"
            )

            if (
                step.job_id is not None
                and step.step_order is not None
            ):
                self.workflow_service.update_selector(
                    step.job_id,
                    step.step_order,
                    healed,
                )

                logger.info(
                    "Updated healed selector in database."
                )

            step.selector = healed

            await action(healed)

            return healing_result.to_dict()
    async def dispatch(
        self,
        step: WorkflowStep,
        execute_child=None,
        branch_path: str | None = None,
    ):
        action = step.action.lower()

        if action == "goto":
            if not step.value:
                raise ValueError(
                    "goto requires 'value'"
                )

            await self.browser.navigator.goto(
                step.value,
                timeout=step.timeout,
            )

            return None

        elif action == "click":
            if not step.selector:
                raise ValueError(
                    "click requires 'selector'"
                )

            return await self._execute_with_healing(
                step,
                lambda selector: self.browser.actions.click(
                    selector,
                    timeout=step.timeout,
                ),
            )

        elif action == "fill":
            if not step.selector or step.value is None:
                raise ValueError(
                    "fill requires 'selector' and 'value'"
                )

            return await self._execute_with_healing(
                step,
                lambda selector: self.browser.actions.fill(
                    selector,
                    step.value,
                    timeout=step.timeout,
                ),
            )

        elif action == "press":
            if not step.selector or step.value is None:
                raise ValueError(
                    "press requires 'selector' and 'value'"
                )

            return await self._execute_with_healing(
                step,
                lambda selector: self.browser.actions.press(
                    selector,
                    step.value,
                    timeout=step.timeout,
                ),
            )

        elif action == "hover":
            if not step.selector:
                raise ValueError(
                    "hover requires 'selector'"
                )

            return await self._execute_with_healing(
                step,
                lambda selector: self.browser.actions.hover(
                    selector,
                    timeout=step.timeout,
                ),
            )

        elif action == "wait_element":
            if not step.selector:
                raise ValueError(
                    "wait_element requires 'selector'"
                )

            return await self._execute_with_healing(
                step,
                lambda selector: self.browser.waits.element(
                    selector,
                    timeout=step.timeout,
                ),
            )

        elif action == "wait_url":
            if not step.value:
                raise ValueError(
                    "wait_url requires 'value'"
                )

            await self.browser.waits.url(
                step.value,
                timeout=step.timeout,
            )

            return None

        elif action == "extract_text":
            if not step.selector:
                raise ValueError(
                    "extract_text requires 'selector'"
                )

            text = await self._execute_with_healing(
                step,
                lambda selector: self.browser.extractor.text(
                    selector,
                ),
            )

            # _execute_with_healing returns healing metadata,
            # so perform extraction separately when needed.
            if isinstance(text, dict):
                healed_info = text
                extracted_text = await self.browser.extractor.text(
                    step.selector,
                )
            else:
                healed_info = None
                extracted_text = text

            logger.info(
                f"Extracted Text: {extracted_text}"
            )

            if step.value:
                self.variables.set(
                    step.value,
                    extracted_text,
                )

            return healed_info

        elif action == "extract_html":
            html = await self.browser.extractor.html()

            logger.info(
                f"Extracted HTML:\n{html}"
            )

            return None

        elif action == "extract_attribute":
            if not step.selector or not step.value:
                raise ValueError(
                    "extract_attribute requires "
                    "'selector' and 'value'"
                )

            result = await self._execute_with_healing(
                step,
                lambda selector: self.browser.extractor.attribute(
                    selector,
                    step.value,
                ),
            )

            if isinstance(result, dict):
                healed_info = result
                value = await self.browser.extractor.attribute(
                    step.selector,
                    step.value,
                )
            else:
                healed_info = None
                value = result

            logger.info(
                f"Extracted Attribute: {value}"
            )

            return healed_info

        elif action == "screenshot":
            if not step.path:
                raise ValueError(
                    "screenshot requires 'path'"
                )

            await self.browser.screenshots.capture_page(
                step.path,
            )

            return None

        elif action == "if":
            if step.condition is None:
                raise ValueError(
                    "if action requires 'condition'"
                )

            left, op, right = step.condition.split()

            left = self.variables.resolve(left)
            right = right.strip("'").strip('"')

            if self.condition_evaluator.evaluate(
                left,
                op,
                right,
            ):
                logger.info(
                    "Condition evaluated TRUE"
                )

                for child in step.true_steps:
                    child_path = (
                        f"{branch_path}.true"
                        if branch_path
                        else "true"
                    )

                    if execute_child is not None:
                        await execute_child(
                            child,
                            branch_path=child_path,
                        )
                    else:
                        await self.dispatch(
                            child,
                            branch_path=child_path,
                        )

            else:
                logger.info(
                    "Condition evaluated FALSE"
                )

                for child in step.false_steps:
                    child_path = (
                        f"{branch_path}.false"
                        if branch_path
                        else "false"
                    )

                    if execute_child is not None:
                        await execute_child(
                            child,
                            branch_path=child_path,
                        )
                    else:
                        await self.dispatch(
                            child,
                            branch_path=child_path,
                        )

            return None

        else:
            raise ValueError(
                f"Unsupported workflow action: {step.action}"
            )
