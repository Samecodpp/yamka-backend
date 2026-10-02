from __future__ import annotations
import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, Float, String
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..core.database import Base

if TYPE_CHECKING:
    from .features_model import FeaturesModel


class AnomalyModel(Base):
    __tablename__ = "anomalies"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    device_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False, index=True
    )
    detected_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    is_anomaly: Mapped[bool] = mapped_column(Boolean, nullable=False)
    detection_confidence: Mapped[float] = mapped_column(Float, nullable=False)
    anomaly_class: Mapped[str | None] = mapped_column(String(64), nullable=True)
    severity: Mapped[str | None] = mapped_column(String(32), nullable=True)
    classification_confidence: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )
    severity_confidence: Mapped[float | None] = mapped_column(Float, nullable=True)
    anomaly_metadata: Mapped[dict | None] = mapped_column(
        "metadata", JSONB, nullable=True
    )

    features: Mapped["FeaturesModel"] = relationship(
        "FeaturesModel", back_populates="anomaly", uselist=False, lazy="joined"
    )
