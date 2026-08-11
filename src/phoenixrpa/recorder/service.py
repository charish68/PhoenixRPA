import json

from phoenixrpa.core.logger import logger
from phoenixrpa.recorder.models import RecordedStep


class RecorderService:

    def __init__(self):
        self.steps: list[RecordedStep] = []
        self.is_recording = False

    # ============================================================
    # START
    # ============================================================

    def start(self):
        """Start recording."""

        self.steps.clear()
        self.is_recording = True

        logger.info("Recorder service started")

    # ============================================================
    # STOP
    # ============================================================

    def stop(self):
        """Stop recording."""

        self.is_recording = False

        logger.info("Recorder service stopped")

    # ============================================================
    # NORMALIZE VALUE
    # ============================================================

    def _normalize_value(
        self,
        value: str | None,
    ) -> str | None:

        if value is None:
            return None

        value = str(value).strip()

        # Handle Markdown mailto:
        #
        # [charish@gmail.com](mailto:charish@gmail.com)
        #
        # [charish@gmail.com](mailto\:charish@gmail.com)

        if value.startswith("[") and "](" in value:

            close_bracket = value.find("](")

            if close_bracket > 0 and value.endswith(")"):

                display_value = value[
                    1:close_bracket
                ].strip()

                if "@" in display_value:
                    return display_value

        return value

    # ============================================================
    # RECORD
    # ============================================================

    def record(
        self,
        action: str,
        selector: str | None = None,
        value: str | None = None,
        path: str | None = None,
    ):
        """Record one browser event."""

        # --------------------------------------------------------
        # Ignore events when recorder is stopped
        # --------------------------------------------------------

        if not self.is_recording:

            logger.debug(
                "Ignoring action because recorder "
                f"is stopped: {action}"
            )

            return

        # --------------------------------------------------------
        # Normalize value
        # --------------------------------------------------------

        value = self._normalize_value(value)

        # --------------------------------------------------------
        # Prevent duplicate consecutive events
        # --------------------------------------------------------

        if self.steps:

            previous = self.steps[-1]

            if (
                previous.action == action
                and previous.selector == selector
                and previous.value == value
                and previous.path == path
            ):

                logger.debug(
                    "Ignoring duplicate consecutive event: "
                    f"{action} {selector}"
                )

                return

        # --------------------------------------------------------
        # Store event
        # --------------------------------------------------------

        self.steps.append(
            RecordedStep(
                action=action,
                selector=selector,
                value=value,
                path=path,
            )
        )

        logger.info(
            f"Recorded action: {action}"
        )

    # ============================================================
    # CLEAR
    # ============================================================

    def clear(self):
        self.steps.clear()

    # ============================================================
    # EXPORT
    # ============================================================

    def export(
        self,
        file: str,
    ):
        """Export recorded workflow as JSON."""

        data = []

        for index, step in enumerate(
            self.steps,
            start=1,
        ):

            data.append(
                {
                    "step_order": index,
                    "action": step.action,
                    "selector": step.selector,
                    "value": self._normalize_value(
                        step.value
                    ),
                    "path": step.path,
                    "timeout": 30000,
                    "retries": 0,
                }
            )

        with open(
            file,
            "w",
            encoding="utf-8",
        ) as f:

            json.dump(
                data,
                f,
                indent=4,
                ensure_ascii=False,
            )

        logger.success(
            f"Workflow exported to {file}"
        )