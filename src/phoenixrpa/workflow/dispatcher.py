from sqlalchemy.orm import Session

from phoenixrpa.browser.manager import BrowserManager
from phoenixrpa.core.logger import logger
from phoenixrpa.services.workflow_service import WorkflowService
from phoenixrpa.workflow.condition import ConditionEvaluator
from phoenixrpa.workflow.models import WorkflowStep
from phoenixrpa.workflow.variables import VariableResolver
from phoenixrpa.workflow.actions import SUPPORTED_ACTIONS


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

    def _resolve_value(self, value):
        if value is None:
            return None

        return self.variables.resolve(value)

    async def dispatch(
        self,
        step: WorkflowStep,
        execute_child=None,
        branch_path: str | None = None,
    ):
        action = step.action.lower()

        if action not in SUPPORTED_ACTIONS:
            raise ValueError(
            f"Unsupported workflow action: {step.action}"
        )

        if action == "goto":
            if not step.value:
                raise ValueError(
                    "goto requires 'value'"
                )

            resolved_value = self._resolve_value(step.value)

            await self.browser.navigator.goto(
                resolved_value,
                timeout=step.timeout,
            )

            return None

        elif action == "click":
            if not step.selector:
                raise ValueError(
                    "click requires 'selector'"
                )

            original_selector = step.selector
            resolved_selector = self._resolve_value(
                original_selector
            )

            step.selector = resolved_selector

            try:
                return await self._execute_with_healing(
                    step,
                    lambda selector: self.browser.actions.click(
                        selector,
                        timeout=step.timeout,
                    ),
                )
            finally:
                step.selector = original_selector
        elif action == "fill":
            if not step.selector or step.value is None:
                raise ValueError(
                    "fill requires 'selector' and 'value'"
                )

            original_selector = step.selector
            resolved_selector = self._resolve_value(
                original_selector
            )
            resolved_value = self._resolve_value(
                step.value
            )

            step.selector = resolved_selector

            try:
                return await self._execute_with_healing(
                    step,
                    lambda selector: self.browser.actions.fill(
                        selector,
                        resolved_value,
                        timeout=step.timeout,
                    ),
                )
            finally:
                step.selector = original_selector
        elif action == "press":
            if not step.selector or step.value is None:
                raise ValueError(
                    "press requires 'selector' and 'value'"
                )

            original_selector = step.selector
            resolved_selector = self._resolve_value(
                original_selector
            )
            resolved_value = self._resolve_value(
                step.value
            )

            step.selector = resolved_selector

            try:
                return await self._execute_with_healing(
                    step,
                    lambda selector: self.browser.actions.press(
                        selector,
                        resolved_value,
                        timeout=step.timeout,
                    ),
                )
            finally:
                step.selector = original_selector
        elif action == "hover":
            if not step.selector:
                raise ValueError(
                    "hover requires 'selector'"
                )

            original_selector = step.selector
            resolved_selector = self._resolve_value(
                original_selector
            )

            step.selector = resolved_selector

            try:
                return await self._execute_with_healing(
                    step,
                    lambda selector: self.browser.actions.hover(
                        selector,
                        timeout=step.timeout,
                    ),
                )
            finally:
                step.selector = original_selector
        elif action == "wait_text":
            if not step.value:
                raise ValueError(
                    "wait_text requires 'value'"
                )

            resolved_value = self.variables.resolve(
                step.value
            )

            await self.browser.waits.text(
                resolved_value,
                timeout=step.timeout,
            )

            return None

        elif action == "wait_url":
            if not step.value:
                raise ValueError(
                    "wait_url requires 'value'"
                )

            resolved_value = self.variables.resolve(
                step.value
            )

            await self.browser.waits.url(
                resolved_value,
                timeout=step.timeout,
            )

            return None

        elif action == "wait_element":
            if not step.selector:
                raise ValueError(
                    "wait_element requires 'selector'"
                )

            resolved_selector = self._resolve_value(
                step.selector
            )

            original_selector = step.selector
            step.selector = resolved_selector

            try:
                return await self._execute_with_healing(
                    step,
                    lambda selector: self.browser.waits.element(
                        selector,
                        timeout=step.timeout,
                    ),
                )
            finally:
                step.selector = original_selector
        elif action == "extract_text":
            if not step.selector:
                raise ValueError(
                    "extract_text requires 'selector'"
                )

            if not step.value:
                raise ValueError(
                    "extract_text requires variable name in 'value'"
                )

            resolved_selector = self._resolve_value(
                step.selector
            )

            original_selector = step.selector
            step.selector = resolved_selector

            extracted_value = None

            async def extract(selector):
                nonlocal extracted_value

                extracted_value = (
                    await self.browser.extractor.text(
                        selector
                    )
                )

            try:
                await self._execute_with_healing(
                    step,
                    extract,
                )
            finally:
                step.selector = original_selector

            if extracted_value is None:
                raise ValueError(
                    f"Unable to extract text from "
                    f"'{resolved_selector}'"
                )

            self.variables.set(
                step.value,
                extracted_value,
            )

            logger.info(
                f"Extracted Text: {extracted_value}"
            )

            logger.success(
                f"Stored extracted text in variable "
                f"'{step.value}'"
            )

            return extracted_value
        elif action == "extract_attribute":
            if not step.selector:
                raise ValueError(
                    "extract_attribute requires 'selector'"
                )

            if not step.attribute:
                raise ValueError(
                    "extract_attribute requires 'attribute'"
                )

            if not step.value:
                raise ValueError(
                    "extract_attribute requires variable name "
                    "in 'value'"
                )

            resolved_selector = self._resolve_value(
                step.selector
            )

            original_selector = step.selector
            step.selector = resolved_selector

            extracted_value = None

            async def extract(selector):
                nonlocal extracted_value

                extracted_value = (
                    await self.browser.extractor.attribute(
                        selector,
                        step.attribute,
                    )
                )

            try:
                await self._execute_with_healing(
                    step,
                    extract,
                )
            finally:
                step.selector = original_selector

            if extracted_value is None:
                raise ValueError(
                    f"Attribute '{step.attribute}' was not found "
                    f"for selector '{resolved_selector}'"
                )

            self.variables.set(
                step.value,
                extracted_value,
            )

            logger.success(
                f"Extracted attribute '{step.attribute}' "
                f"into variable '{step.value}'"
            )

            return extracted_value
        elif action == "extract_table":
            if not step.selector:
                raise ValueError(
                    "extract_table requires 'selector'"
                )

            if not step.value:
                raise ValueError(
                    "extract_table requires variable name "
                    "in 'value'"
                )

            original_selector = step.selector
            resolved_selector = self.variables.resolve(
                original_selector
            )

            extracted_table = None

            async def extract(selector):
                nonlocal extracted_table

                extracted_table = (
                    await self.browser.extractor.table(
                        selector
                    )
                )

            step.selector = resolved_selector

            try:
                await self._execute_with_healing(
                    step,
                    extract,
                )
            finally:
                step.selector = original_selector

            if extracted_table is None:
                raise ValueError(
                    f"Unable to extract table from "
                    f"'{resolved_selector}'"
                )

            self.variables.set(
                step.value,
                extracted_table,
            )

            logger.success(
                f"Extracted table into variable "
                f"'{step.value}'"
            )

            return extracted_table
        elif action == "extract_html":
            extracted_html = (
                await self.browser.extractor.html()
            )

            logger.info(
                f"Extracted HTML:\n{extracted_html}"
            )

            if step.value:
                self.variables.set(
                    step.value,
                    extracted_html,
                )

                logger.success(
                    f"Extracted HTML into variable "
                    f"'{step.value}'"
                )

            return extracted_html
        elif action == "screenshot":
            if not step.path:
                raise ValueError(
                    "screenshot requires 'path'"
                )

            resolved_path = self._resolve_value(
                step.path
            )

            await self.browser.screenshots.capture_page(
                resolved_path,
            )

            return None
        elif action == "if":
            if step.condition is None:
                raise ValueError(
                    "if action requires 'condition'"
                )

            parts = step.condition.split(maxsplit=2)

            if len(parts) != 3:
                raise ValueError(
                    "if condition must contain "
                    "left operator right"
                )

            left, op, right = parts

            left = self.variables.resolve(left)
            right = right.strip("'").strip('"')
            right = self.variables.resolve(right)

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














