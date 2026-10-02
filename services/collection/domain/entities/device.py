from dataclasses import dataclass, field
from uuid import UUID

from ..value_objects import MACAddress, TelemetryWindow
from ..events import Event, TelemetryCollected


@dataclass
class Device:
    name: str
    mac: MACAddress
    id: UUID | None = None
    _events: list[Event] = field(
        default_factory=list,
        init=False,
        repr=False
    )

    def collect_telemetry(self, telemetry: TelemetryWindow) -> None:
        self._events.append(
            TelemetryCollected(
                device_id=self.id,
                telemetry=telemetry
            )
        )

    def pop_events(self) -> list[Event]:
        events, self._events = self._events, []
        return events
