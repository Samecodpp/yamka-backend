from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .anomaly_repo import IAnomalyRepository
    from .features_repo import IFeaturesRepository


class ITransaction(ABC):
    """Unit of Work: manages a single DB transaction and vends repositories."""

    @abstractmethod
    async def __aenter__(self) -> "ITransaction": ...

    @abstractmethod
    async def __aexit__(self, exc_type, exc, tb) -> None: ...

    @property
    @abstractmethod
    def anomaly_repo(self) -> "IAnomalyRepository": ...

    @property
    @abstractmethod
    def features_repo(self) -> "IFeaturesRepository": ...
