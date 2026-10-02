from abc import ABC, abstractmethod

from ..events import Event


class IOutboxRepository(ABC):

    @abstractmethod
    async def add(self, event: Event) -> None: ...
