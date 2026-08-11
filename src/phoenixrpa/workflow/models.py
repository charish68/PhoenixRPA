from dataclasses import dataclass, field


@dataclass
class WorkflowStep:
    action: str

    selector: str | None = None
    value: str | None = None
    path: str | None = None

    timeout: int = 30000
    retries: int = 0

    # Metadata
    job_id: int | None = None
    step_order: int = 0

    # Future features
    condition: str | None = None
    true_steps: list["WorkflowStep"] = field(default_factory=list)
    false_steps: list["WorkflowStep"] = field(default_factory=list)


@dataclass
class Workflow:
    steps: list[WorkflowStep]