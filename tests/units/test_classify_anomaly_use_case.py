from unittest.mock import MagicMock

from services.classification.application.use_cases.classify_anomaly_use_case import (
    ClassifyAnomalyUseCase,
)
from services.classification.application.dto.input import ClassifyAnomalyInput
from services.classification.domain.value_objects.feature_vector import FeaturesVector
from services.classification.domain.value_objects.classifier_result import (
    ClassifierResult,
)


def test_classify_anomaly_returns_correct_output():
    norm_features = FeaturesVector(values=[0.2, 0.8])

    normalizer = MagicMock()
    normalizer.normalize.return_value = norm_features

    classifier = MagicMock()
    classifier.classify.return_value = ClassifierResult(
        anomaly_class=2,
        confidence=0.87,
        metadata={"label": "pothole"},
    )

    use_case = ClassifyAnomalyUseCase(normalizer=normalizer, classifier=classifier)
    input_dto = ClassifyAnomalyInput(features={"accel_x": 1.0, "accel_y": 0.8})

    output = use_case.execute(input_dto)

    assert output.anomaly_class == 2
    assert output.confidence == 0.87
    assert output.metadata == {"label": "pothole"}
    normalizer.normalize.assert_called_once()
    classifier.classify.assert_called_once_with(norm_features)
