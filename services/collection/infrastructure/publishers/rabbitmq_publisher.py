import aio_pika
from aio_pika import RobustConnection

from ...domain.interfaces import IEventPublisher
from ...domain.events.event import Event
from ..mappers import EventMapper


class RabbitMQPublisher(IEventPublisher):
    def __init__(self, connection: RobustConnection, exchange_name: str) -> None:
        self._connection = connection
        self._exchange_name = exchange_name
        self._mapper = EventMapper()

    async def publish(self, event: Event) -> None:
        message_body = self._mapper.to_message(event)
        async with self._connection.channel() as channel:
            exchange = await channel.declare_exchange(
                self._exchange_name,
                aio_pika.ExchangeType.TOPIC,
                durable=True,
            )
            await exchange.publish(
                aio_pika.Message(
                    body=message_body.encode(),
                    content_type="application/json",
                    delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
                ),
                routing_key="telemetry.collected",
            )
