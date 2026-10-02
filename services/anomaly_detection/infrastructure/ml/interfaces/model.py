from abc import ABC, abstractmethod
import numpy as np

class IModel(ABC):

    @abstractmethod
    def predict_proba(self, X: np.ndarray) -> np.ndarray: ...

    @abstractmethod
    def predict(self, X: np.ndarray) -> np.ndarray: ...

    @property
    @abstractmethod
    def metadata(self) -> dict[str, str]: ...
