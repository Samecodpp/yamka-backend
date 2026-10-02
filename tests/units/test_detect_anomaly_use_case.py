from unittest.mock import MagicMock

from services.anomaly_detection.application.use_cases.detect_anomaly_use_case import (
    DetectAnomalyUseCase,
)
from services.anomaly_detection.application.dto.input import DetectAnomalyInput
from services.anomaly_detection.domain.value_objects.feature_vector import (
    FeaturesVector,
)
from services.anomaly_detection.domain.value_objects.detector_result import (
    DetectorResult,
)


def test_detect_anomaly_returns_correct_output():
    norm_features = FeaturesVector(values=[0.1, 0.5, 0.9])

    normalizer = MagicMock()
    normalizer.normalize.return_value = norm_features

    detector = MagicMock()
    detector.detect.return_value = DetectorResult(
        is_anomaly=True,
        confidence=0.95,
        metadata={"model": "isolation_forest"},
    )

    use_case = DetectAnomalyUseCase(normalizer=normalizer, detector=detector)
    input_dto = DetectAnomalyInput(
        features={"accel_x": 1.0, "accel_y": 0.5, "accel_z": 0.9}
    )

    output = use_case.execute(input_dto)

    assert output.is_anomaly is True
    assert output.confidence == 0.95
    assert output.metadata == {"model": "isolation_forest"}
    normalizer.normalize.assert_called_once()
    detector.detect.assert_called_once_with(norm_features)
