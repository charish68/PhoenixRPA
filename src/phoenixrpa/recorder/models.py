from dataclasses import dataclass


@dataclass
class RecordedStep:
    action: str

    selector: str | None = None

    value: str | None = None

    path: str | None = None