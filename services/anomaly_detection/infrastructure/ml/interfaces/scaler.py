from abc import ABC, abstractmethod
import numpy as np

class IScaler(ABC):

    @abstractmethod
    def transform(self, X: np.ndarray) -> np.ndarray: ...


