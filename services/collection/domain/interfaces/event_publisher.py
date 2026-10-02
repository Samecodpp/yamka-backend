from abc import ABC, abstractmethod

from ..events.event import Event


class IEventPublisher(ABC):

    @abstractmethod
    async def publish(self, event: Event) -> None: ...
