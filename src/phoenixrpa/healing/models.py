from dataclasses import dataclass


@dataclass
class ElementCandidate:
    selector: str
    score: float