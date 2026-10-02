from datetime import datetime

from pydantic import BaseModel, Field


class IngestTelemetriesRequest(BaseModel):
    timestamp_start: datetime
    device_mac: str = Field(examples=["AA:BB:CC:DD:EE:FF"])
    device_name: str = Field(examples=["sensor-01"])
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    speed_rate: int = Field(gt=0, description="Speed sampling rate (Hz)")
    sample_rate: int = Field(gt=0, description="IMU sampling rate (Hz)")
    speed: list[float] = Field(min_length=1)
    accel_x: list[float] = Field(min_length=1)
    accel_y: list[float] = Field(min_length=1)
    accel_z: list[float] = Field(min_length=1)
    gyro_x: list[float] = Field(min_length=1)
    gyro_y: list[float] = Field(min_length=1)
    gyro_z: list[float] = Field(min_length=1)
    vibration_adc: list[float] = Field(min_length=1)
