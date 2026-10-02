from abc import ABC, abstractmethod
from uuid import UUID

from ..entities import Features, Anomaly


class IDetectionPort(ABC):

    @abstractmethod
    async def detect(self, device_id: UUID, features: Features) -> Anomaly: ...
