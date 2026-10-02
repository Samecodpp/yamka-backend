from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4

from ..events import Event
from ..value_objects import AnomalyClass, AnomalySeverity


@dataclass
class Anomaly:
    device_id: UUID
    is_anomaly: bool
    detection_confidence: float
    id: UUID = field(default_factory=uuid4)
    detected_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: dict = field(default_factory=dict)
    anomaly_class: AnomalyClass | None = None
    severity: AnomalySeverity | None = None
    classification_confidence: float | None = None
    severity_confidence: float | None = None

    def set_metadata(self, metadata_key: str, metadata: dict) -> None:
        self.metadata[metadata_key] = metadata

    def classify(
        self,
        anomaly_class: AnomalyClass,
        classification_confidence: float,
        metadata_key: str,
        metadata: dict,
    ) -> "Anomaly":
        self.anomaly_class = anomaly_class
        self.classification_confidence = classification_confidence
        self.set_metadata(metadata_key, metadata)
        return self
