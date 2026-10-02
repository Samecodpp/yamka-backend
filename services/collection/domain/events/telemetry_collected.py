from dataclasses import dataclass
from uuid import UUID

from .event import Event
from ..value_objects import TelemetryWindow


@dataclass(frozen=True, kw_only=True)
class TelemetryCollected(Event):
    device_id: UUID
    telemetry: TelemetryWindow
