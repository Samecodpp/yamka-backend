from sqlalchemy.ext.asyncio import AsyncSession

from ...domain.entities.features import Features, FeatureName
from ...domain.interfaces import IFeaturesRepository
from ...domain.value_objects import AccFeature, GyroFeature, CrossFeature
from ..models.features_model import FeaturesModel


def _str_to_feature_name(key: str) -> FeatureName:
    for cls in (AccFeature, GyroFeature, CrossFeature):
        try:
            return cls(key)
        except ValueError:
            continue
    raise ValueError(f"Unknown feature key: {key!r}")


class FeaturesRepository(IFeaturesRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, features: Features) -> Features:
        model = self._to_model(features)
        self._session.add(model)
        await self._session.flush()
        return features

    def _to_model(self, entity: Features) -> FeaturesModel:
        return FeaturesModel(
            id=entity.id,
            anomaly_id=entity.anomaly_id,
            values={str(k): v for k, v in entity.values.items()},
        )

    def _to_entity(self, model: FeaturesModel) -> Features:
        return Features(
            id=model.id,
            anomaly_id=model.anomaly_id,
            values={_str_to_feature_name(k): v for k, v in model.values.items()},
        )
