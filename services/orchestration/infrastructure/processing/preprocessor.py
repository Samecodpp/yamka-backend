import numpy as np
from scipy.signal import butter, filtfilt

from ...domain.interfaces import IStep


class Preprocessor(IStep[dict, dict]):
    SPEED_MIN = 2.0
    GRAVITY = 9.807
    ACC_BAND_LOW_HZ = 0.5
    ACC_BAND_HIGH_HZ = 30.0
    GYRO_BAND_LOW_HZ = 0.3
    GYRO_BAND_HIGH_HZ = 20.0
    FILTER_ORDER = 4

    def fit(self, X: dict, y=None) -> "Preprocessor":
        return self

    def transform(self, X: dict) -> dict:
        window = X
        interp_speed = self._interpolate_speed(window)
        filtered = self._filter_signals(window)
        signal_names = ("accel_x", "accel_y", "accel_z", "gyro_x", "gyro_y", "gyro_z")
        present = [n for n in signal_names if n in filtered]
        if present:
            min_len = min(len(filtered[n]) for n in present)
            min_len = min(min_len, len(interp_speed))
            for n in present:
                filtered[n] = filtered[n][:min_len]
            interp_speed = interp_speed[:min_len]
        normalized = self.normalize_by_speed(filtered, interp_speed)
        normalized["speed"] = interp_speed
        return normalized

    def _interpolate_speed(self, window: dict) -> np.ndarray:
        return np.interp(
            window["imu_timestamp"], window["speed_timestamp"], window["speed"]
        )

    def _filter_signals(self, window: dict) -> dict:
        filtered_window = window.copy()
        signal_names = ("accel_x", "accel_y", "accel_z", "gyro_x", "gyro_y", "gyro_z")
        fs = float(window["imu_hz"])

        for name in signal_names:
            if name not in window:
                continue

            sig = window[name]

            if name == "accel_z":
                sig = sig - self.GRAVITY

            if "accel" in name:
                low_hz = self.ACC_BAND_LOW_HZ
                high_hz = self.ACC_BAND_HIGH_HZ
            else:
                low_hz = self.GYRO_BAND_LOW_HZ
                high_hz = self.GYRO_BAND_HIGH_HZ

            filtered_window[name] = self._bandpass(sig, low_hz, high_hz, fs)

        return filtered_window

    def _bandpass(self, signal: np.ndarray, low_hz: float, high_hz: float, fs: float):
        nyq = 0.5 * fs
        low = max(low_hz / nyq, 1e-4)
        high = min(high_hz / nyq, 0.999)

        if not (0 < low < high < 1):
            return signal - np.mean(signal)

        b, a = butter(self.FILTER_ORDER, [low, high], btype="band")
        padlen = 3 * (max(len(a), len(b)) - 1)

        if signal.size <= padlen:
            return signal - np.mean(signal)

        return filtfilt(b, a, signal)

    def normalize_by_speed(self, window: dict, speed: np.ndarray) -> dict:
        normalized_window = window.copy()
        signal_names = ("accel_x", "accel_y", "accel_z", "gyro_x", "gyro_y", "gyro_z")

        speed_floor = np.maximum(speed, self.SPEED_MIN)

        for name in signal_names:
            if name in window:
                normalized_window[name] = window[name] / speed_floor

        return normalized_window
