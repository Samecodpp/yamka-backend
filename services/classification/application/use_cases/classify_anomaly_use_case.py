from ..dto.input import ClassifyAnomalyInput
from ..dto.output import ClassifyAnomalyOutput

from ...domain.interfaces import IClassifier, INormalizer
from ...domain.value_objects import FeaturesVector


class ClassifyAnomalyUseCase:
    def __init__(self, normalizer: INormalizer, classifier: IClassifier) -> None:
        self._normalizer = normalizer
        self._classifier = classifier

    def execute(self, input: ClassifyAnomalyInput) -> ClassifyAnomalyOutput:
        features = FeaturesVector.from_dict(input.features)
        norm_features = self._normalizer.normalize(features)
        result = self._classifier.classify(norm_features)
        return ClassifyAnomalyOutput(
            anomaly_class=result.anomaly_class,
            confidence=result.confidence,
            metadata=result.metadata,
        )
