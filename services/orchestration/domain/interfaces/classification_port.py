from abc import ABC, abstractmethod
from uuid import UUID

from ..entities import Features, Anomaly


class IClassificationPort(ABC):

    @abstractmethod
    async def classify(self, anomaly: Anomaly, features: Features) -> Anomaly: ...
