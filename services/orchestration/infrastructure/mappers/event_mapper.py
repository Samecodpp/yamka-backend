import json
from datetime import datetime

import numpy as np

from ...domain.interfaces.mapper import IMapper


class EventMapper(IMapper[bytes | str, dict]):

    def map(self, source: bytes | str) -> dict:
        raw = json.loads(source)
        tel = raw["telemetry"]

        t0 = datetime.fromisoformat(tel["timestamp_start"]).timestamp()
        sample_rate: int = tel["sample_rate"]
        speed_rate: int = tel["speed_rate"]

        n_imu = len(tel["accel"]["x"])
        n_speed = len(tel["speed"])

        imu_timestamps = np.array([t0 + i / sample_rate for i in range(n_imu)])
        speed_timestamps = np.array([t0 + i / speed_rate for i in range(n_speed)])

        return {
            "event_id": raw["event_id"],
            "occurred_at": raw["occurred_at"],
            "device_id": raw["device_id"],
            "accel": tel["accel"],
            "gyro": tel["gyro"],
            "speed": tel["speed"],
            "time": {
                "imu_timestamp": imu_timestamps,
                "speed_timestamp": speed_timestamps,
            },
            "sample_rate": sample_rate,
            "speed_rate": speed_rate,
        }

    @classmethod
    def from_message(cls, body: bytes | str) -> dict:
        return cls().map(body)
