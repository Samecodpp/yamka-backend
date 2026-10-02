from __future__ import annotations
import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..core.database import Base

if TYPE_CHECKING:
    from .anomaly_model import AnomalyModel


class FeaturesModel(Base):
    __tablename__ = "features"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    anomaly_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("anomalies.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )
    values: Mapped[dict] = mapped_column(JSONB, nullable=False)

    anomaly: Mapped["AnomalyModel"] = relationship(
        "AnomalyModel", back_populates="features"
    )
