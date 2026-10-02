import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
for _noisy in ("sqlalchemy", "botocore", "boto3", "urllib3"):
    logging.getLogger(_noisy).setLevel(logging.WARNING)

from .presentation.exception_handler import register_exception_handlers
from .infrastructure.core import database
from .infrastructure.core.message_broker import (
    init_rabbitmq_conn,
    close_rabbitmq_connection,
)
from .presentation.api.ingestion_router import router as ingestion_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    database.init_engine()
    await init_rabbitmq_conn()
    engine = database.get_engine()
    from .infrastructure.models.device import DeviceModel

    async with engine.begin() as conn:
        await conn.run_sync(database.Base.metadata.create_all)
    yield
    await close_rabbitmq_connection()
    await engine.dispose()


app = FastAPI(title="Collection Service", lifespan=lifespan)
register_exception_handlers(app)
app.include_router(ingestion_router)
