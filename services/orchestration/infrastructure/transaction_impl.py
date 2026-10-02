from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from ..domain.interfaces import ITransaction, IAnomalyRepository, IFeaturesRepository
from .repositories.anomaly_repo_impl import AnomalyRepository
from .repositories.features_repo_impl import FeaturesRepository


class SQLAlchemyTransaction(ITransaction):
    def __init__(self, session_factory: async_sessionmaker) -> None:
        self._session_factory = session_factory
        self._session: AsyncSession | None = None
        self._anomaly_repo: IAnomalyRepository | None = None
        self._features_repo: IFeaturesRepository | None = None

    async def __aenter__(self) -> "SQLAlchemyTransaction":
        self._session = self._session_factory()
        self._anomaly_repo = AnomalyRepository(self._session)
        self._features_repo = FeaturesRepository(self._session)
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        if self._session is None:
            return
        if exc_type:
            await self._session.rollback()
        else:
            await self._session.commit()
        await self._session.close()
        self._session = None
        self._anomaly_repo = None
        self._features_repo = None

    @property
    def anomaly_repo(self) -> IAnomalyRepository:
        if self._anomaly_repo is None:
            raise RuntimeError("Transaction not started — use 'async with' first")
        return self._anomaly_repo

    @property
    def features_repo(self) -> IFeaturesRepository:
        if self._features_repo is None:
            raise RuntimeError("Transaction not started — use 'async with' first")
        return self._features_repo
