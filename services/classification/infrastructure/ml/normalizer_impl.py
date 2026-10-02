import numpy as np

from ...domain.interfaces.normalizer import INormalizer
from ...domain.value_objects import FeaturesVector
from .exported_model import ExportedNormalizer


class Normalizer(INormalizer):

    def __init__(self, normalizer: ExportedNormalizer) -> None:
        self._normalizer = normalizer

    def normalize(self, features: FeaturesVector) -> FeaturesVector:
        X = np.array(features.values).reshape(1, -1)
        X_norm = self._normalizer.transform(X)
        return FeaturesVector(values=X_norm[0].tolist())
