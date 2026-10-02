from dataclasses import dataclass


@dataclass(frozen=True)
class DetectAnomalyInput:
    features: dict[str, float]
