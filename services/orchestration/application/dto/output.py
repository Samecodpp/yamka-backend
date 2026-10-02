from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from ...domain.value_objects import AnomalyClass, AnomalySeverity


@dataclass(frozen=True)
class ProcessTelemetryOutput:
    anomaly_id: UUID
    features_id: UUID
    device_id: UUID
    detected_at: datetime
    is_anomaly: bool
    detection_confidence: float
    anomaly_class: AnomalyClass | None = None
    severity: AnomalySeverity | None = None
    classification_metadata: dict | None = None
