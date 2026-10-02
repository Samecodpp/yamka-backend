from dataclasses import dataclass


@dataclass(frozen=True)
class FeaturesVector:
    values: list[float]

    def __post_init__(self):
        if not self.values:
            raise ValueError("FeatureVector cannot be empty")

    @classmethod
    def from_dict(cls, features: dict[str, float]) -> "FeaturesVector":
        return FeaturesVector(values=[value for value in features.values()])
