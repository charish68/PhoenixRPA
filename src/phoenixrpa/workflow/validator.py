
from phoenixrpa.workflow.actions import SUPPORTED_ACTIONS
from phoenixrpa.workflow.condition import ConditionEvaluator
from phoenixrpa.workflow.models import Workflow, WorkflowStep


class WorkflowValidationError(ValueError):
    """Raised when a workflow is invalid."""


class WorkflowValidator:

    def validate(self, workflow: Workflow) -> None:
        """Validate the complete workflow.

        Raises:
            WorkflowValidationError: If any workflow step is invalid.
        """

        if not workflow.steps:
            raise WorkflowValidationError(
                "Workflow cannot be empty."
            )

        for index, step in enumerate(
            workflow.steps,
            start=1,
        ):
            self._validate_step(
                step,
                index,
            )

    def _validate_step(
        self,
        step: WorkflowStep,
        index,
    ) -> None:

        # --------------------------------------------------
        # Action
        # --------------------------------------------------

        if not isinstance(step.action, str):
            raise WorkflowValidationError(
                f"Step {index}: action must be a string."
            )

        if not step.action.strip():
            raise WorkflowValidationError(
                f"Step {index}: action is required."
            )

        action = step.action.strip().lower()
        step.action = action

        if action not in SUPPORTED_ACTIONS:
            raise WorkflowValidationError(
                f"Step {index}: unsupported action "
                f"'{step.action}'."
            )

        # --------------------------------------------------
        # Timeout
        # --------------------------------------------------

        if not isinstance(step.timeout, (int, float)):
            raise WorkflowValidationError(
                f"Step {index}: timeout must be a number."
            )

        if step.timeout <= 0:
            raise WorkflowValidationError(
                f"Step {index}: timeout must be greater "
                f"than 0."
            )

        # --------------------------------------------------
        # Retries
        # --------------------------------------------------

        if not isinstance(step.retries, (int, float)):
            raise WorkflowValidationError(
                f"Step {index}: retries must be a number."
            )

        if step.retries < 0:
            raise WorkflowValidationError(
                f"Step {index}: retries cannot be negative."
            )

        # --------------------------------------------------
        # Action-specific validation
        # --------------------------------------------------

        if action == "goto":

            self._require_value(
                step,
                index,
                "goto",
            )

        elif action == "click":

            self._require_selector(
                step,
                index,
                "click",
            )

        elif action == "fill":

            self._require_selector(
                step,
                index,
                "fill",
            )

            self._require_value(
                step,
                index,
                "fill",
            )

        elif action == "press":

            self._require_selector(
                step,
                index,
                "press",
            )

            self._require_value(
                step,
                index,
                "press",
            )

        elif action == "hover":

            self._require_selector(
                step,
                index,
                "hover",
            )

        elif action == "wait_element":

            self._require_selector(
                step,
                index,
                "wait_element",
            )

        elif action == "wait_url":

            self._require_value(
                step,
                index,
                "wait_url",
            )

        elif action == "wait_text":

            self._require_value(
                step,
                index,
                "wait_text",
            )

        elif action == "extract_text":

            self._require_selector(
                step,
                index,
                "extract_text",
            )

        elif action == "extract_attribute":

            self._require_selector(
                step,
                index,
                "extract_attribute",
            )

            self._require_value(
                step,
                index,
                "extract_attribute",
            )

        elif action == "screenshot":

            if not step.path:
                raise WorkflowValidationError(
                    f"Step {index}: screenshot requires "
                    f"'path'."
                )

        elif action == "if":

            if (
                step.condition is None
                or not step.condition.strip()
            ):
                raise WorkflowValidationError(
                    f"Step {index}: if requires "
                    f"'condition'."
                )

            self._validate_condition(
                step,
                index,
            )

            for child_index, child in enumerate(
                step.true_steps,
                start=1,
            ):
                self._validate_step(
                    child,
                    f"{index}.true.{child_index}",
                )

            for child_index, child in enumerate(
                step.false_steps,
                start=1,
            ):
                self._validate_step(
                    child,
                    f"{index}.false.{child_index}",
                )

    # ------------------------------------------------------
    # Helpers
    # ------------------------------------------------------

    def _require_selector(
        self,
        step: WorkflowStep,
        index,
        action: str,
    ) -> None:

        if (
            step.selector is None
            or not step.selector.strip()
        ):
            raise WorkflowValidationError(
                f"Step {index}: {action} requires "
                f"'selector'."
            )

    def _require_value(
        self,
        step: WorkflowStep,
        index,
        action: str,
    ) -> None:

        if step.value is None:
            raise WorkflowValidationError(
                f"Step {index}: {action} requires "
                f"'value'."
            )

    def _validate_condition(
        self,
        step: WorkflowStep,
        index,
    ) -> None:

        try:
            ConditionEvaluator().parse(
                step.condition
            )
        except ValueError as error:
            raise WorkflowValidationError(
                f"Step {index}: {error}"
            ) from error


# ----------------------------------------------------------
# Unit Tests
# ----------------------------------------------------------




