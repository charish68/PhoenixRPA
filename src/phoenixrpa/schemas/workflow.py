from pydantic import BaseModel, ConfigDict


class WorkflowStepCreate(BaseModel):
    step_order: int
    action: str

    selector: str | None = None
    value: str | None = None
    path: str | None = None

    timeout: int = 30000
    retries: int = 0

    condition: str | None = None

    true_steps: list["WorkflowStepCreate"] = []
    false_steps: list["WorkflowStepCreate"] = []


class WorkflowStepResponse(BaseModel):
    id: int
    job_id: int
    step_order: int

    action: str

    selector: str | None = None
    value: str | None = None
    path: str | None = None

    timeout: int
    retries: int

    condition: str | None = None

    model_config = ConfigDict(from_attributes=True)
