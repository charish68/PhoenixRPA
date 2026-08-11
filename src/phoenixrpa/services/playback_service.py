import json
from pathlib import Path

from phoenixrpa.core.logger import logger
from phoenixrpa.workflow.models import WorkflowStep
from phoenixrpa.workflow.dispatcher import WorkflowDispatcher


class PlaybackService:

    def __init__(self, dispatcher: WorkflowDispatcher):
        self.dispatcher = dispatcher

    async def play(
        self,
        workflow_path: str,
    ):
        """
        Load a recorded workflow JSON file
        and execute every step sequentially.
        """

        path = Path(workflow_path)

        if not path.exists():
            raise FileNotFoundError(
                f"Workflow file not found: {workflow_path}"
            )

        logger.info(
            f"Loading workflow: {workflow_path}"
        )

        with path.open(
            "r",
            encoding="utf-8",
        ) as file:
            workflow_data = json.load(file)

        if not isinstance(workflow_data, list):
            raise ValueError(
                "Workflow JSON must contain a list of steps."
            )

        logger.info(
            f"Loaded {len(workflow_data)} workflow steps"
        )

        for item in workflow_data:

            step = WorkflowStep(
                **item
            )

            logger.info(
                f"Executing step "
                f"{step.step_order}: "
                f"{step.action}"
            )

            await self.dispatcher.dispatch(
                step
            )

        logger.success(
            "Workflow playback completed successfully"
        )