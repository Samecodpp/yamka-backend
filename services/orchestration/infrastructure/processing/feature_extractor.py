import numpy as np
from scipy.stats import kurtosis, skew
from scipy.signal import find_peaks

from ...domain.interfaces import IStep
from ...domain.entities.features import Features, _ALL_FEATURES, FeatureName


class FeatureExtractor(IStep[dict, np.ndarray]):

    ALL_FEATURES: list[FeatureName] = _ALL_FEATURES

    def fit(self, X: np.ndarray, y: np.ndarray | None = None) -> "FeatureExtractor":
        return self

    def transform(self, X: dict) -> np.ndarray:
        window = X
        features: list[float] = []

        accel_names = ("accel_x", "accel_y", "accel_z")
        gyro_names = ("gyro_x", "gyro_y", "gyro_z")
        fs = float(window["imu_hz"])

        for name in accel_names:
            features.extend(self._acc_features(window[name], fs))

        for name in gyro_names:
            features.extend(self._gyro_features(window[name]))

        features.extend(
            self._cross_features(
                tuple(window[n] for n in accel_names),
                tuple(window[n] for n in gyro_names),
                fs=fs,
            )
        )

        return np.array(features, dtype=np.float32)

    def _acc_features(self, acc: np.ndarray, fs: float) -> list[float]:
        abs_acc = np.abs(acc)
        peak = float(abs_acc.max())
        rms = float(np.sqrt(np.mean(acc**2)))
        kurt = float(kurtosis(acc))
        skewness = float(skew(acc))
        jerk_max = float(np.abs(np.diff(acc) * fs).max()) if len(acc) > 1 else 0.0
        p1, p2, p3, dom = self._fft_features(acc, fs)
        shape = self._impulse_shape(acc)
        extra = self._extra_acc_features(acc, fs)

        return [peak, rms, kurt, skewness, jerk_max, p1, p2, p3, dom, *shape, *extra]

    def _impulse_shape(self, acc: np.ndarray) -> list[float]:
        n = len(acc)
        if n == 0:
            return [0.0, 0.0, 1.0, 0.0]

        eps = 1e-8
        abs_acc = np.abs(acc)
        peak_idx = int(np.argmax(abs_acc))
        peak = float(abs_acc[peak_idx])

        threshold = 0.5 * peak
        above = np.where(abs_acc >= threshold)[0]

        if len(above) < 2:
            rise_time = float(peak_idx / n)
            decay_time = float((n - 1 - peak_idx) / n)
            impulse_width = float(1.0 / n)
        else:
            ev_start = int(above[0])
            ev_end = int(above[-1])
            ev_len = ev_end - ev_start + 1

            local_peak = peak_idx - ev_start
            rise_time = float(local_peak / (ev_len + eps))
            decay_time = float((ev_end - peak_idx) / (ev_len + eps))
            impulse_width = float(ev_len / n)

        symmetry = rise_time / (decay_time + eps)
        return [rise_time, decay_time, symmetry, impulse_width]

    def _extra_acc_features(self, acc: np.ndarray, fs: float) -> list[float]:
        n = len(acc)
        eps = 1e-8

        abs_acc = np.abs(acc)
        peak_idx = int(np.argmax(abs_acc))
        peak_val = float(abs_acc[peak_idx])
        peak_signed = float(acc[peak_idx])
        pos_area = float(np.sum(acc[acc > 0]))
        neg_area = float(np.abs(np.sum(acc[acc < 0])))
        pos_neg_ratio = pos_area / (neg_area + eps)

        if n > 1:
            signs = np.sign(acc)
            signs[signs == 0] = 1
            zero_cross_rate = float(np.sum(np.diff(signs) != 0) / (n - 1))
        else:
            zero_cross_rate = 0.0

        energy_before = float(np.mean(acc[:peak_idx] ** 2)) if peak_idx > 0 else 0.0
        energy_after = float(np.mean(acc[peak_idx:] ** 2)) if peak_idx < n else 0.0
        pre_post_ratio = energy_before / (energy_after + eps)

        median_abs = float(np.median(abs_acc))
        peak_prominence = peak_val / (median_abs + eps)

        min_height = 0.2 * peak_val if peak_val > eps else None
        min_dist = max(1, int(0.05 * n))
        peaks_pos, _ = find_peaks(acc, height=min_height, distance=min_dist)
        peaks_neg, _ = find_peaks(-acc, height=min_height, distance=min_dist)
        n_peaks = float((len(peaks_pos) + len(peaks_neg)) / n)

        return [
            peak_signed,
            pos_neg_ratio,
            zero_cross_rate,
            pre_post_ratio,
            peak_prominence,
            n_peaks,
        ]

    def _gyro_features(self, gyro: np.ndarray) -> list[float]:
        peak = float(np.abs(gyro).max())
        rms = float(np.sqrt(np.mean(gyro**2)))
        kurt = float(kurtosis(gyro, nan_policy="omit"))
        kurt = float(np.nan_to_num(kurt, nan=0.0, posinf=0.0, neginf=0.0))
        return [peak, rms, kurt]

    def _cross_features(
        self,
        acc_signals: tuple[np.ndarray, np.ndarray, np.ndarray],
        gyro_signals: tuple[np.ndarray, np.ndarray, np.ndarray],
        fs: float,
    ) -> list[float]:
        ax, ay, az = acc_signals
        eps = 1e-8

        accel_mag = np.sqrt(ax**2 + ay**2 + az**2)

        horiz_rms = float(np.sqrt(np.mean(ax**2 + ay**2)))
        vert_rms = float(np.sqrt(np.mean(az**2)))

        feats: list[float] = [
            float(accel_mag.max()),
            float(np.sqrt(np.mean(accel_mag**2))),
        ]

        gx, gy, gz = gyro_signals
        gyro_mag = np.sqrt(gx**2 + gy**2 + gz**2)
        feats.append(float(gyro_mag.max()))
        feats.append(float(np.sqrt(np.mean(gyro_mag**2))))
        feats.append(vert_rms / (horiz_rms + eps))
        feats.append(self._spectral_centroid(az, fs))
        feats.append(self._safe_corr(ax, ay))
        feats.append(self._safe_corr(ax, az))
        feats.append(self._safe_corr(ay, az))
        feats.append(float(kurtosis(accel_mag)))
        feats.append(float(skew(accel_mag)))
        mag_peak_idx = int(np.argmax(accel_mag))
        feats.append(float(np.sign(az[mag_peak_idx])))
        _, p1_z, _, _ = self._fft_features_raw(az, fs)
        _, p1_mag, _, _ = self._fft_features_raw(accel_mag, fs)
        feats.append(p1_z / (p1_mag + eps))

        # частка вікна де magnitude перевищує 1.5 * median
        median_mag = float(np.median(accel_mag))
        threshold = 1.5 * median_mag
        feats.append(float(np.sum(accel_mag > threshold) / len(accel_mag)))

        return feats

    def _fft_features(
        self, signal: np.ndarray, fs: float
    ) -> tuple[float, float, float, float]:
        freqs = np.fft.rfftfreq(len(signal), d=1.0 / fs)
        amp = np.abs(np.fft.rfft(signal))
        total = amp.sum() + 1e-10
        p1 = float(amp[(freqs >= 1) & (freqs < 5)].sum() / total)
        p2 = float(amp[(freqs >= 5) & (freqs < 15)].sum() / total)
        p3 = float(amp[(freqs >= 15) & (freqs < 30)].sum() / total)
        return p1, p2, p3, float(freqs[amp.argmax()])

    def _fft_features_raw(
        self, signal: np.ndarray, fs: float
    ) -> tuple[float, float, float, float]:
        freqs = np.fft.rfftfreq(len(signal), d=1.0 / fs)
        amp = np.abs(np.fft.rfft(signal))
        p1 = float(amp[(freqs >= 1) & (freqs < 5)].sum())
        p2 = float(amp[(freqs >= 5) & (freqs < 15)].sum())
        p3 = float(amp[(freqs >= 15) & (freqs < 30)].sum())
        return p1, p2, p3, float(freqs[amp.argmax()])

    def _spectral_centroid(self, signal: np.ndarray, fs: float) -> float:
        freqs = np.fft.rfftfreq(len(signal), d=1.0 / fs)
        amp = np.abs(np.fft.rfft(signal))
        return float((freqs * amp).sum() / (amp.sum() + 1e-10))

    def _safe_corr(self, a: np.ndarray, b: np.ndarray) -> float:
        """Pearson correlation; returns 0.0 when either signal has zero variance."""
        if len(a) < 2:
            return 0.0
        std_a = float(np.std(a))
        std_b = float(np.std(b))
        if std_a < 1e-10 or std_b < 1e-10:
            return 0.0
        return float(np.corrcoef(a, b)[0, 1])

    @staticmethod
    def _safe_corr(a: np.ndarray, b: np.ndarray) -> float:
        if len(a) < 2:
            return 0.0
        std_a = float(np.std(a))
        std_b = float(np.std(b))
        if std_a < 1e-10 or std_b < 1e-10:
            return 0.0
        return float(np.corrcoef(a, b)[0, 1])

    @staticmethod
    def acc_mask() -> np.ndarray:
        acc_names = set(Features.acc_feature_names())
        return np.array([f in acc_names for f in _ALL_FEATURES])

    @staticmethod
    def gyro_mask() -> np.ndarray:
        gyro_names = set(Features.gyro_feature_names())
        return np.array([f in gyro_names for f in _ALL_FEATURES])
