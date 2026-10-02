import numpy as np


class ExportedNormalizer:
    """Wrapper навколо StandardScaler для classification сервісу."""

    def __init__(self, scaler, metadata: dict[str, str]) -> None:
        self.scaler = scaler
        self.metadata = metadata

    def transform(self, X: np.ndarray) -> np.ndarray:
        return self.scaler.transform(X)


class ExportedModel:
    """Wrapper навколо multiclass estimator для classification сервісу."""

    def __init__(self, estimator, threshold: float, metadata: dict[str, str]) -> None:
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
