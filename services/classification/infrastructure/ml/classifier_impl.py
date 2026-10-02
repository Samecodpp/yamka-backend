import numpy as np

from ...domain.interfaces import IClassifier
from ...domain.value_objects import ClassifierResult, FeaturesVector
from .exported_model import ExportedModel


class Classifier(IClassifier):

    def __init__(self, model: ExportedModel) -> None:
        self._model = model

    def classify(self, features: FeaturesVector) -> ClassifierResult:
        X = np.array(features.values).reshape(1, -1)
        anomaly_class = self._model.predict_class(X)
        confidence = self._model.predict_confidence(X)
        return ClassifierResult(
            anomaly_class=anomaly_class,
            confidence=confidence,
            metadata=self._model.metadata,
        )
