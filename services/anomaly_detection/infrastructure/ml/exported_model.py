import numpy as np


class ExportedNormalizer:
    """Wrapper навколо StandardScaler. Збережений окремим .joblib файлом.
    Цей файл ПОВИНЕН бути ідентичним в training-коді та в бекенді."""

    def __init__(self, scaler, metadata: dict[str, str]) -> None:
        self.scaler = scaler  # StandardScaler
        self.metadata = metadata

    def transform(self, X: np.ndarray) -> np.ndarray:
        return self.scaler.transform(X)


class ExportedModel:
    """Wrapper навколо estimator без scaler. Збережений окремим .joblib файлом.
    Цей файл ПОВИНЕН бути ідентичним в training-коді та в бекенді."""

    def __init__(self, estimator, threshold: float, metadata: dict[str, str]) -> None:
        self.estimator = (
            estimator  # LogisticRegression / LGBMClassifier / XGBClassifier
        )
        self.threshold = threshold
        self.metadata = metadata

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        return self.estimator.predict_proba(X)

    def predict(self, X: np.ndarray) -> np.ndarray:
        probs = self.predict_proba(X)[:, 1]
        return (probs >= self.threshold).astype(int)
