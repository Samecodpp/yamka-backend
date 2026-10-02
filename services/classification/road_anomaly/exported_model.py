"""Compatibility shim — classes referenced by the pickled classification model.
The ML artifacts were pickled under the 'road_anomaly.exported_model' namespace."""

import numpy as np


class ExportedNormalizer:
    def __init__(self, scaler, metadata: dict) -> None:
        self.scaler = scaler
        self.metadata = metadata

    def transform(self, X: np.ndarray) -> np.ndarray:
        return self.scaler.transform(X)


class ExportedModel:
    def __init__(self, estimator, threshold: float, metadata: dict) -> None:
        self.estimator = estimator
        self.threshold = threshold
        self.metadata = metadata

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        return self.estimator.predict_proba(X)

    def predict_class(self, X: np.ndarray) -> int:
        probs = self.predict_proba(X)[0]
        return int(np.argmax(probs))

    def predict_confidence(self, X: np.ndarray) -> float:
        probs = self.predict_proba(X)[0]
        return float(np.max(probs))
