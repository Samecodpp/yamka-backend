from dataclasses import dataclass


@dataclass(frozen=True)
class ClassifierResult:
    anomaly_class: int
    confidence: float
    metadata: dict[str, str]
