from dataclasses import dataclass


@dataclass(frozen=True)
class ClassifyAnomalyOutput:
    anomaly_class: int
    confidence: float
    metadata: dict[str, str]
