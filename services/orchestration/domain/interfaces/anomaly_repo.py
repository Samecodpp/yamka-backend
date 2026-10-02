from abc import ABC, abstractmethod
from uuid import UUID

from ..entities.anomaly import Anomaly

class IAnomalyRepository(ABC):

    @abstractmethod
    async def create(self, anomaly: Anomaly) -> Anomaly | None: ...

    @abstractmethod
    async def get_by_id(self, id: UUID) -> Anomaly | None: ...

    @abstractmethod
    async def update(self, id: UUID, payload: dict) -> Anomaly | None: ...
