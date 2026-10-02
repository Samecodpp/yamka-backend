from dataclasses import dataclass
from datetime import datetime

from .geoposition import Geoposition


@dataclass(frozen=True)
class TelemetryWindow:
    geoposition: Geoposition
    timestamp_start: datetime
    sample_rate: int
    speed_rate: int
    speed: list[float]
    accel_x: list[float]
    accel_y: list[float]
    accel_z: list[float]
    gyro_x: list[float]
    gyro_y: list[float]
    gyro_z: list[float]
    vibration_adc: list[float]
