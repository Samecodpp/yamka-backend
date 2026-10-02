import aio_pika
from aio_pika import RobustConnection

from .settings import get_settings

_rabbitmq_connection: RobustConnection | None = None


async def init_rabbitmq_conn() -> None:
    global _rabbitmq_connection

    if _rabbitmq_connection is None:
        settings = get_settings()

        _rabbitmq_connection = await aio_pika.connect_robust(url=settings.RABBITMQ_URL)


def get_rabbitmq_conn() -> RobustConnection:
    if _rabbitmq_connection is None:
        raise RuntimeError("RabbitMQ connection not initialized")

    return _rabbitmq_connection


async def close_rabbitmq_connection() -> None:
    global _rabbitmq_connection

    if _rabbitmq_connection is not None:
        await _rabbitmq_connection.close()
        _rabbitmq_connection = None


############################################################################################

# import aioboto3

# from .settings import get_settings

# _sqs_session: aioboto3.Session | None = None


# def init_sqs_session() -> None:
#     global _sqs_session
#     if _sqs_session is None:
#         settings = get_settings()
#         _sqs_session = aioboto3.Session(
#             region_name=settings.AWS_REGION,
#         )


# def get_sqs_session() -> aioboto3.Session:
#     if _sqs_session is None:
#         raise RuntimeError("SQS session not initialized")
#     return _sqs_session
