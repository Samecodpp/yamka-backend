from abc import ABC, abstractmethod

from ..entities.features import Features


class IFeaturesRepository(ABC):

    @abstractmethod
    async def create(self, features: Features) -> Features: ...
