import numpy as np

from ...domain.interfaces import IDetector
from ...domain.value_objects import DetectorResult, FeaturesVector
from .exported_model import ExportedModel


class Detector(IDetector):

    def __init__(self, model: ExportedModel) -> None:
        self._model = model

    def detect(self, features: FeaturesVector) -> DetectorResult:
        X = np.array(features.values).reshape(1, -1)
        is_anomaly = bool(self._model.predict(X)[0])
        confidence = float(self._model.predict_proba(X)[0, 1])
        return DetectorResult(
            is_anomaly=is_anomaly,
            confidence=confidence,
            metadata=self._model.metadata,
        )
