from __future__ import annotations
from abc import ABC, abstractmethod

from .device_repo import IDeviceRepository


class ITransaction(ABC):
    device: IDeviceRepository

    @abstractmethod
    async def __aenter__(self) -> ITransaction: ...

    @abstractmethod
    async def __aexit__(self, exc_type, exc, tb) -> None: ...

    @abstractmethod
    async def __aenter__(self) -> ITransaction: ...

    @abstractmethod
    async def __aexit__(self, exc_type, exc, tb) -> None: ...
