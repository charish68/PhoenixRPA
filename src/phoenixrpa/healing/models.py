from dataclasses import dataclass


@dataclass
class ElementCandidate:
    selector: str
    score: float


@dataclass
class HealingResult:
    status: str
    original_selector: str
    healed_selector: str | None = None
    method: str | None = None
    confidence: float | None = None

    def to_dict(self) -> dict:
        return {
            "status": self.status,
            "original_selector": self.original_selector,
            "healed_selector": self.healed_selector,
            "method": self.method,
            "confidence": self.confidence,
        }
