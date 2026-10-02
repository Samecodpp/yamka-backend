from enum import Enum


class CrossFeature(str, Enum):
    ACCEL_MAG_MAX = "accel_mag_max"
    ACCEL_MAG_RMS = "accel_mag_rms"
    GYRO_MAG_MAX = "gyro_mag_max"
    GYRO_MAG_RMS = "gyro_mag_rms"
    VERT_HORIZ_RMS_RATIO = "vert_horiz_rms_ratio"
    ACC_Z_SPECTRAL_CENTROID = "acc_z_spectral_centroid"
    ACC_XY_CORRELATION = "acc_xy_correlation"
    ACC_XZ_CORRELATION = "acc_xz_correlation"
    ACC_YZ_CORRELATION = "acc_yz_correlation"
    ACC_MAG_KURT = "acc_mag_kurt"
    ACC_MAG_SKEW = "acc_mag_skew"
    ACC_MAG_PEAK_SIGNED_Z = "acc_mag_peak_signed_z"
    ACC_Z_P1_RATIO_TO_MAG = "acc_z_p1_ratio_to_mag"
    IMPACT_DURATION_RATIO = "impact_duration_ratio"
