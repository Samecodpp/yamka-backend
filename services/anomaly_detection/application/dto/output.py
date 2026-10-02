from dataclasses import dataclass


@dataclass(frozen=True)
class DetectAnomalyOutput:
    is_anomaly: bool
    confidence: float
    metadata: dict[str, str]
