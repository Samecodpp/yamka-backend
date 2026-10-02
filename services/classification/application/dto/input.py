from dataclasses import dataclass


@dataclass(frozen=True)
class ClassifyAnomalyInput:
    features: dict[str, float]
