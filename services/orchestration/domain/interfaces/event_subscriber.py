from abc import ABC, abstractmethod
from typing import TypeAlias, Awaitable, Callable

EventHandler: TypeAlias = Callable[[dict], Awaitable[None]]


class IEventSubscriber(ABC):

    @abstractmethod
    async def subscribe(
        self,
        routing_key: str,
        handler: EventHandler,
    ) -> None:
        pass

    @abstractmethod
    async def start_consuming(self) -> None:
        pass

    @abstractmethod
    async def stop_consuming(self) -> None:
        pass
