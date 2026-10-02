from abc import ABC, abstractmethod
from ..value_objects import DetectorResult, FeaturesVector


class IDetector(ABC):

    @abstractmethod
    def detect(self, features: FeaturesVector) -> DetectorResult: ...
