from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from ...domain.entities.anomaly import Anomaly
from ...domain.interfaces import IAnomalyRepository
from ...domain.value_objects import AnomalyClass, AnomalySeverity
from ..models.anomaly_model import AnomalyModel


class AnomalyRepository(IAnomalyRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, anomaly: Anomaly) -> Anomaly:
        model = self._to_model(anomaly)
        self._session.add(model)
        await self._session.flush()
        return anomaly

    async def get_by_id(self, id: UUID) -> Anomaly | None:
        stmt = select(AnomalyModel).where(AnomalyModel.id == id)
        model = await self._session.scalar(stmt)
        if model is None:
            return None
        return self._to_entity(model)

    async def update(self, id: UUID, payload: dict) -> Anomaly | None:
        stmt = (
            update(AnomalyModel)
            .where(AnomalyModel.id == id)
            .values(**payload)
            .returning(AnomalyModel)
        )
        model = await self._session.scalar(stmt)
        if model is None:
            return None
        return self._to_entity(model)

    def _to_model(self, entity: Anomaly) -> AnomalyModel:
        return AnomalyModel(
            id=entity.id,
            device_id=entity.device_id,
            detected_at=entity.detected_at,
            is_anomaly=entity.is_anomaly,
            detection_confidence=entity.detection_confidence,
            anomaly_class=entity.anomaly_class.value if entity.anomaly_class else None,
            severity=entity.severity.value if entity.severity else None,
            classification_confidence=entity.classification_confidence,
            severity_confidence=entity.severity_confidence,
            anomaly_metadata=entity.metadata,
        )

    def _to_entity(self, model: AnomalyModel) -> Anomaly:
        return Anomaly(
            id=model.id,
            device_id=model.device_id,
            detected_at=model.detected_at,
            is_anomaly=model.is_anomaly,
            detection_confidence=model.detection_confidence,
            anomaly_class=(
                AnomalyClass(model.anomaly_class)
                if model.anomaly_class is not None
                else None
            ),
            severity=(
                AnomalySeverity(model.severity) if model.severity is not None else None
            ),
            classification_confidence=model.classification_confidence,
            severity_confidence=model.severity_confidence,
            metadata=model.anomaly_metadata,
        )
