import json

from ...domain.events import TelemetryCollected
from ...domain.events.event import Event


class EventMapper:

    def to_message(self, event: Event) -> str:
        if isinstance(event, TelemetryCollected):
            return json.dumps(
                {
                    "event_type": "telemetry.collected",
                    "event_id": str(event.id),
                    "occurred_at": event.occurred_at.isoformat(),
                    "device_id": str(event.device_id),
                    "telemetry": {
                        "geoposition": {
                            "latitude": event.telemetry.geoposition.latitude,
                            "longitude": event.telemetry.geoposition.longitude,
                        },
                        "timestamp_start": event.telemetry.timestamp_start.isoformat(),
                        "sample_rate": event.telemetry.sample_rate,
                        "speed_rate": event.telemetry.speed_rate,
                        "speed": event.telemetry.speed,
                        "accel": {
                            "x": event.telemetry.accel_x,
                            "y": event.telemetry.accel_y,
                            "z": event.telemetry.accel_z,
                        },
                        "gyro": {
                            "x": event.telemetry.gyro_x,
                            "y": event.telemetry.gyro_y,
                            "z": event.telemetry.gyro_z,
                        },
                        "vibration_adc": event.telemetry.vibration_adc,
                    },
                }
            )
        raise ValueError(f"Unknown event type: {type(event)}")
