from dataclasses import dataclass


@dataclass
class SelectorCandidate:
    selector: str
    score: float