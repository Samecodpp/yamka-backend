from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

import numpy as np


@dataclass
class ProcessTelemetryInput:

    event_id: UUID
    occurred_at: datetime
    device_id: UUID
    sample_rate: int
    speed_rate: int
    speed: list[float]
    accel_x: list[float]
    accel_y: list[float]
    accel_z: list[float]
    gyro_x: list[float]
    gyro_y: list[float]
    gyro_z: list[float]
    imu_timestamp: np.ndarray
    speed_timestamp: np.ndarray

    @classmethod
    def from_event(cls, raw: dict) -> "ProcessTelemetryInput":
        return cls(
            event_id=UUID(raw["event_id"]),
            occurred_at=datetime.fromisoformat(raw["occurred_at"]),
            device_id=UUID(raw["device_id"]),
            sample_rate=int(raw["sample_rate"]),
            speed_rate=int(raw["speed_rate"]),
            speed=raw["speed"],
            accel_x=raw["accel"]["x"],
            accel_y=raw["accel"]["y"],
            accel_z=raw["accel"]["z"],
            gyro_x=raw["gyro"]["x"],
            gyro_y=raw["gyro"]["y"],
            gyro_z=raw["gyro"]["z"],
            imu_timestamp=raw["time"]["imu_timestamp"],
            speed_timestamp=raw["time"]["speed_timestamp"],
        )
