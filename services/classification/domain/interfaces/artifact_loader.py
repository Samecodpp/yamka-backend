from abc import ABC, abstractmethod
from typing import Any


class IArtifactLoader(ABC):

    @abstractmethod
    def load_model(self) -> Any: ...

    @abstractmethod
    def load_scaler(self) -> Any: ...
