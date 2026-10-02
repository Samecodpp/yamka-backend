import aioboto3

from ...domain.events.event import Event
from ...domain.interfaces import IEventPublisher
from ..mappers.event_mapper import EventMapper


class SQSEventPublisher(IEventPublisher):
    def __init__(
        self,
        queue_url: str,
        session: aioboto3.Session,
    ) -> None:
        self._queue_url = queue_url
        self._session = session
        self._mapper = EventMapper()

    async def publish(self, event: Event) -> None:
        message_body = self._mapper.to_message(event)
        async with self._session.client("sqs") as sqs:
            await sqs.send_message(
                QueueUrl=self._queue_url,
                MessageBody=message_body,
            )
