from typing import Annotated
from fastapi import Depends

from ..infrastructure.core.database import async_sessionmaker, get_session_factory
from ..infrastructure.core.settings import Settings, get_settings
from ..infrastructure.core.message_broker import get_rabbitmq_conn
from ..infrastructure.transaction_impl import SQLAlchemyTransaction
from ..infrastructure.publishers import RabbitMQPublisher
from ..application.use_cases.collect_data_use_case import CollectDataUseCase


def get_transaction(
    session_factory: Annotated[async_sessionmaker, Depends(get_session_factory)],
) -> SQLAlchemyTransaction:
    return SQLAlchemyTransaction(session_factory=session_factory)


def get_publisher(
    settings: Annotated[Settings, Depends(get_settings)],
) -> RabbitMQPublisher:
    return RabbitMQPublisher(
        connection=get_rabbitmq_conn(),
        exchange_name="telemetry",
    )


def get_collect_data_use_case(
    transaction: Annotated[SQLAlchemyTransaction, Depends(get_transaction)],
    publisher: Annotated[RabbitMQPublisher, Depends(get_publisher)],
) -> CollectDataUseCase:
    return CollectDataUseCase(transaction=transaction, publisher=publisher)
