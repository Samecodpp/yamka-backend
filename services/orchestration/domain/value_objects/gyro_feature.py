from enum import Enum


class GyroFeature(str, Enum):
    X_PEAK = "gyro_x_peak"
    X_RMS = "gyro_x_rms"
    X_KURT = "gyro_x_kurt"

    Y_PEAK = "gyro_y_peak"
    Y_RMS = "gyro_y_rms"
    Y_KURT = "gyro_y_kurt"

    Z_PEAK = "gyro_z_peak"
    Z_RMS = "gyro_z_rms"
    Z_KURT = "gyro_z_kurt"
