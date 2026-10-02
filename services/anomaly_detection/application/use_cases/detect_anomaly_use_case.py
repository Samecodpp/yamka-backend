from ..dto.input import DetectAnomalyInput
from ..dto.output import DetectAnomalyOutput

from ...domain.interfaces import IDetector, INormalizer
from ...domain.value_objects import FeaturesVector


class DetectAnomalyUseCase:
    def __init__(self, normalizer: INormalizer, detector: IDetector) -> None:
        self._normalizer = normalizer
        self._detector = detector

    def execute(self, input: DetectAnomalyInput) -> DetectAnomalyOutput:
        features = FeaturesVector.from_dict(input.features)
        norm_features = self._normalizer.normalize(features)
        result = self._detector.detect(norm_features)
        return DetectAnomalyOutput(
            is_anomaly=result.is_anomaly,
            confidence=result.confidence,
            metadata=result.metadata,
        )
