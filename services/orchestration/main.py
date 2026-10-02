import asyncio
import logging
import signal

from .infrastructure.core import database
from .infrastructure.core.message_broker import (
    init_rabbitmq_conn,
    close_rabbitmq_connection,
    get_rabbitmq_conn,
)
from .infrastructure.core.database import get_session_factory
from .infrastructure.core.settings import get_settings
from .infrastructure.transaction_impl import SQLAlchemyTransaction
from .infrastructure.mappers import ProcessorMapper
from .infrastructure.processing.preprocessor import Preprocessor
from .infrastructure.processing.feature_extractor import FeatureExtractor
from .infrastructure.subscribers.rabbitmq_subscriber import RabbitMQSubscriber
from .infrastructure.adapters import ClassificationAdapter, DetectionAdapter
from .application.use_cases.processing_telemetry_use_case import (
    ProcessingTelemetryUseCase,
)
from .presentation.handler.telemetry_handler import make_telemetry_handler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
for _noisy in ("sqlalchemy", "aio_pika", "aiormq", "botocore", "boto3"):
    logging.getLogger(_noisy).setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

EXCHANGE_NAME = "telemetry"
QUEUE_NAME = "orchestration.telemetry.collected"


async def main() -> None:
    database.init_engine()
    await init_rabbitmq_conn()
    from .infrastructure.models.anomaly_model import AnomalyModel
    from .infrastructure.models.features_model import FeaturesModel

    async with database.get_engine().begin() as conn:
        await conn.run_sync(database.Base.metadata.create_all)

    session_factory = get_session_factory()
    transaction = SQLAlchemyTransaction(session_factory)

    settings = get_settings()

    subscriber = RabbitMQSubscriber(
        connection=get_rabbitmq_conn(),
        exchange_name=EXCHANGE_NAME,
        queue_name=QUEUE_NAME,
        prefetch_count=10,
    )

    detection_adapter = DetectionAdapter(settings.DETECTOR_SERVICE_GRPC_HOST)
    classification_adapter = ClassificationAdapter(
        settings.CLASSIFIER_SERVICE_GRPC_HOST
    )

    use_case = ProcessingTelemetryUseCase(
        transaction=transaction,
        subscriber=subscriber,
        mapper=ProcessorMapper(),
        preprocessor=Preprocessor(),
        feature_extractor=FeatureExtractor(),
        detection_port=detection_adapter,
        classification_port=classification_adapter,
    )

    handler = make_telemetry_handler(use_case)
    await subscriber.subscribe(ProcessingTelemetryUseCase.ROUTING_KEY, handler)

    loop = asyncio.get_running_loop()
    stop_event = asyncio.Event()

    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, stop_event.set)

    logger.info("Orchestration service started, consuming messages…")
    consumer_task = asyncio.create_task(subscriber.start_consuming())

    await stop_event.wait()

    logger.info("Shutting down…")
    await subscriber.stop_consuming()
    consumer_task.cancel()
    try:
        await consumer_task
    except asyncio.CancelledError:
        pass

    await close_rabbitmq_connection()
    await database.get_engine().dispose()
    logger.info("Shutdown complete.")


if __name__ == "__main__":
    asyncio.run(main())
