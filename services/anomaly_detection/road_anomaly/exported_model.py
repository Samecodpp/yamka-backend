"""Compatibility shim — classes identical to anomaly_detection.infrastructure.ml.exported_model.
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

    def predict(self, X: np.ndarray) -> np.ndarray:
        probs = self.predict_proba(X)[:, 1]
        return (probs >= self.threshold).astype(int)
