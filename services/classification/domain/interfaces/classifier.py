from abc import ABC, abstractmethod
from ..value_objects import ClassifierResult, FeaturesVector


class IClassifier(ABC):

    @abstractmethod
    def classify(self, features: FeaturesVector) -> ClassifierResult: ...
