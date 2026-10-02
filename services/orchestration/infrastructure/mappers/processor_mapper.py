import numpy as np

from ...application.dto.input import ProcessTelemetryInput
from ...domain.interfaces.mapper import IMapper


class ProcessorMapper(IMapper[ProcessTelemetryInput, dict]):
    """Maps ProcessTelemetryInput DTO to the flat numpy-array dict
    expected by Preprocessor.transform()."""

    def map(self, source: ProcessTelemetryInput) -> dict:
        return {
            "accel_x": np.asarray(source.accel_x, dtype=float),
            "accel_y": np.asarray(source.accel_y, dtype=float),
            "accel_z": np.asarray(source.accel_z, dtype=float),
            "gyro_x": np.asarray(source.gyro_x, dtype=float),
            "gyro_y": np.asarray(source.gyro_y, dtype=float),
            "gyro_z": np.asarray(source.gyro_z, dtype=float),
            "speed": source.speed,
            "imu_hz": float(source.sample_rate),
            "imu_timestamp": source.imu_timestamp,
            "speed_timestamp": source.speed_timestamp,
        }
