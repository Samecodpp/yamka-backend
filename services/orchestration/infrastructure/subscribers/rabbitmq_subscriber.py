import asyncio
import logging

import aio_pika
from aio_pika import RobustConnection
from aio_pika.abc import AbstractIncomingMessage

from ...domain.interfaces.event_subscriber import IEventSubscriber, EventHandler
from ..mappers import EventMapper

logger = logging.getLogger(__name__)


class RabbitMQSubscriber(IEventSubscriber):
    EXCHANGE_TYPE = aio_pika.ExchangeType.TOPIC

    def __init__(
        self,
        connection: RobustConnection,
        exchange_name: str,
        queue_name: str = "",
        prefetch_count: int = 10,
    ) -> None:
        self._connection = connection
        self._exchange_name = exchange_name
        self._queue_name = queue_name
        self._prefetch_count = prefetch_count
        self._handlers: dict[str, EventHandler] = {}
        self._channel: aio_pika.abc.AbstractChannel | None = None
        self._consuming = False

    async def subscribe(self, routing_key: str, handler: EventHandler) -> None:
        self._handlers[routing_key] = handler

    async def start_consuming(self) -> None:
        self._channel = await self._connection.channel()
        await self._channel.set_qos(prefetch_count=self._prefetch_count)

        exchange = await self._channel.declare_exchange(
            self._exchange_name,
            self.EXCHANGE_TYPE,
            durable=True,
        )

        queue = await self._channel.declare_queue(
            self._queue_name,
            durable=bool(self._queue_name),
            auto_delete=not bool(self._queue_name),
        )

        for routing_key in self._handlers:
            await queue.bind(exchange, routing_key=routing_key)

        self._consuming = True
        await queue.consume(self._dispatch)

        while self._consuming:
            await asyncio.sleep(1)

    async def stop_consuming(self) -> None:
        self._consuming = False
        if self._channel and not self._channel.is_closed:
            await self._channel.close()
            self._channel = None

    async def _dispatch(self, message: AbstractIncomingMessage) -> None:
        async with message.process(requeue=True):
            routing_key = message.routing_key or ""
            handler = self._handlers.get(routing_key)
            if handler is None:
                logger.warning("No handler for routing_key=%s, skipping.", routing_key)
                return

            try:
                payload: dict = EventMapper.from_message(message.body)
            except Exception as e:
                logger.error(
                    "EventMapper failed for routing_key=%s: %s", routing_key, e
                )
                return

            try:
                await handler(payload)
            except Exception as e:
                logger.exception(
                    "Handler for routing_key=%s raised: %s", routing_key, e
                )
                raise
