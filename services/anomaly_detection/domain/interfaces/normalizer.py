from abc import ABC, abstractmethod
from ..value_objects import FeaturesVector


class INormalizer(ABC):

    @abstractmethod
    def normalize(self, features: FeaturesVector) -> FeaturesVector: ...
