from dataclasses import dataclass


@dataclass(frozen=True)
class DetectorResult:
    is_anomaly: bool
    confidence: float
    metadata: dict[str, str]
