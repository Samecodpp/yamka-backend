from dataclasses import dataclass, field
from typing import Union
from uuid import UUID, uuid4

from ..value_objects.acc_feature import AccFeature
from ..value_objects.cross_feature import CrossFeature
from ..value_objects.gyro_feature import GyroFeature

FeatureName = Union[AccFeature, GyroFeature, CrossFeature]

_ALL_FEATURES: list[FeatureName] = (
    list(AccFeature) + list(GyroFeature) + list(CrossFeature)
)

_ACC_CROSS: frozenset[CrossFeature] = frozenset(
    {
        CrossFeature.ACCEL_MAG_MAX,
        CrossFeature.ACCEL_MAG_RMS,
        CrossFeature.VERT_HORIZ_RMS_RATIO,
        CrossFeature.ACC_Z_SPECTRAL_CENTROID,
        CrossFeature.ACC_XY_CORRELATION,
        CrossFeature.ACC_XZ_CORRELATION,
        CrossFeature.ACC_YZ_CORRELATION,
        CrossFeature.ACC_MAG_KURT,
        CrossFeature.ACC_MAG_SKEW,
        CrossFeature.ACC_MAG_PEAK_SIGNED_Z,
        CrossFeature.ACC_Z_P1_RATIO_TO_MAG,
        CrossFeature.IMPACT_DURATION_RATIO,
    }
)

_GYRO_CROSS: frozenset[CrossFeature] = frozenset(
    {
        CrossFeature.GYRO_MAG_MAX,
        CrossFeature.GYRO_MAG_RMS,
    }
)


@dataclass
class Features:
    values: dict[FeatureName, float]
    id: UUID = field(default_factory=uuid4)
    anomaly_id: UUID | None = None

    @staticmethod
    def all_feature_names() -> list[FeatureName]:
        return _ALL_FEATURES

    @staticmethod
    def acc_feature_names() -> list[FeatureName]:
        return [
            f for f in _ALL_FEATURES if isinstance(f, AccFeature) or f in _ACC_CROSS
        ]

    @staticmethod
    def gyro_feature_names() -> list[FeatureName]:
        return [
            f for f in _ALL_FEATURES if isinstance(f, GyroFeature) or f in _GYRO_CROSS
        ]

    def get(self, name: FeatureName) -> float:
        return self.values[name]

    @classmethod
    def from_dict(
        cls, values: dict[str, float]
    ) -> "Features":
        missing = [f for f in _ALL_FEATURES if f not in values]
        if missing:
            raise ValueError(f"Missing features: {missing}")
        typed: dict[FeatureName, float] = {f: values[f] for f in _ALL_FEATURES}
        return cls(values=typed)
