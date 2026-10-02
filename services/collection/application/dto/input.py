from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class CollectDataInput:
    device_mac: str
    device_name: str
    latitude: float
    longitude: float
    speed_rate: int
    sample_rate: int
    timestamp_start: datetime
    speed: list[float]
    accel_x: list[float]
    accel_y: list[float]
    accel_z: list[float]
    gyro_x: list[float]
    gyro_y: list[float]
    gyro_z: list[float]
    vibration_adc: list[float]
