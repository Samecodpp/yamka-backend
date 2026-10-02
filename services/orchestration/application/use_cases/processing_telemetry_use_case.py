import logging
from uuid import uuid4

import numpy as np

from ...domain.entities.anomaly import Anomaly
from ...domain.entities.features import Features
from ...domain.interfaces import (
    IEventSubscriber,
    IStep,
    ITransaction,
    IMapper,
    IDetectionPort,
    IClassificationPort,
)
from ..dto.input import ProcessTelemetryInput
from ..dto.output import ProcessTelemetryOutput

logger = logging.getLogger(__name__)


class ProcessingTelemetryUseCase:
    ROUTING_KEY = "telemetry.collected"

    def __init__(
        self,
        transaction: ITransaction,
        subscriber: IEventSubscriber,
        mapper: IMapper,
        preprocessor: IStep[dict, dict],
        feature_extractor: IStep[dict, np.ndarray],
        detection_port: IDetectionPort,
        classification_port: IClassificationPort,
    ):
        self._transaction = transaction
        self._subscriber = subscriber
        self._preprocessor = preprocessor
        self._feat_extractor = feature_extractor
        self._mapper = mapper
        self._d_port = detection_port
        self._c_port = classification_port

    async def execute(self, input: ProcessTelemetryInput) -> ProcessTelemetryOutput:
        preprocessor_input: dict = self._mapper.map(input)
        processed: dict = self._preprocessor.transform(preprocessor_input)
        features_array: np.ndarray = self._feat_extractor.transform(processed)

        features = Features.from_dict(
            values={
                name: float(features_array[i])
                for i, name in enumerate(Features.all_feature_names())
            }
        )

        anomaly = await self._d_port.detect(
            device_id=input.device_id, features=features
        )

        if anomaly.is_anomaly:
            anomaly = await self._c_port.classify(anomaly=anomaly, features=features)

        features.anomaly_id = anomaly.id
        async with self._transaction as txn:
            await txn.anomaly_repo.create(anomaly)
            await txn.features_repo.create(features)

        return ProcessTelemetryOutput(
            anomaly_id=anomaly.id,
            features_id=features.id,
            device_id=anomaly.device_id,
            detected_at=anomaly.detected_at,
            is_anomaly=anomaly.is_anomaly,
            detection_confidence=anomaly.detection_confidence,
            anomaly_class=anomaly.anomaly_class,
            severity=anomaly.severity,
            classification_metadata=anomaly.metadata,
        )
