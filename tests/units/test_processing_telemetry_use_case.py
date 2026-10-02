import asyncio
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import numpy as np

from services.orchestration.application.use_cases.processing_telemetry_use_case import (
    ProcessingTelemetryUseCase,
)
from services.orchestration.application.dto.input import ProcessTelemetryInput
from services.orchestration.domain.entities.anomaly import Anomaly


class _MockTransaction:
    def __init__(self, anomaly_repo: MagicMock, features_repo: MagicMock) -> None:
        self.anomaly_repo = anomaly_repo
        self.features_repo = features_repo

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        pass


def test_processing_telemetry_detects_and_classifies_anomaly():
    device_id = uuid4()

    mock_anomaly = Anomaly(
        device_id=device_id,
        is_anomaly=True,
        detection_confidence=0.92,
        id=uuid4(),
        detected_at=datetime.now(timezone.utc),
    )

    mock_features = MagicMock()
    mock_features.id = uuid4()
    mock_features.anomaly_id = None

    mapper = MagicMock()
    mapper.map.return_value = {"raw": "data"}

    preprocessor = MagicMock()
    preprocessor.transform.return_value = {"processed": "data"}

    feature_extractor = MagicMock()
    feature_extractor.transform.return_value = np.array([0.1, 0.2])

    detection_port = MagicMock()
    detection_port.detect = AsyncMock(return_value=mock_anomaly)

    classification_port = MagicMock()
    classification_port.classify = AsyncMock(return_value=mock_anomaly)

    anomaly_repo = MagicMock()
    anomaly_repo.create = AsyncMock()

    features_repo = MagicMock()
    features_repo.create = AsyncMock()

    transaction = _MockTransaction(
        anomaly_repo=anomaly_repo, features_repo=features_repo
    )
    subscriber = MagicMock()

    use_case = ProcessingTelemetryUseCase(
        transaction=transaction,
        subscriber=subscriber,
        mapper=mapper,
        preprocessor=preprocessor,
        feature_extractor=feature_extractor,
        detection_port=detection_port,
        classification_port=classification_port,
    )

    input_dto = ProcessTelemetryInput(
        event_id=uuid4(),
        occurred_at=datetime.now(timezone.utc),
        device_id=device_id,
        sample_rate=100,
        speed_rate=10,
        speed=[1.0, 2.0],
        accel_x=[0.1, 0.2],
        accel_y=[0.0, 0.1],
        accel_z=[9.8, 9.7],
        gyro_x=[0.01, 0.02],
        gyro_y=[0.00, 0.01],
        gyro_z=[0.00, 0.00],
        imu_timestamp=np.array([0.0, 0.01]),
        speed_timestamp=np.array([0.0, 0.1]),
    )

    _PATCH_TARGET = (
        "services.orchestration.application.use_cases"
        ".processing_telemetry_use_case.Features"
    )

    async def _run():
        return await use_case.execute(input_dto)

    with patch(_PATCH_TARGET) as MockFeatures:
        MockFeatures.all_feature_names.return_value = ["f1", "f2"]
        MockFeatures.from_dict.return_value = mock_features

        output = asyncio.run(_run())

    assert output.is_anomaly is True
    assert output.anomaly_id == mock_anomaly.id
    assert output.device_id == device_id
    assert output.detection_confidence == 0.92
    detection_port.detect.assert_awaited_once()
    classification_port.classify.assert_awaited_once()
    anomaly_repo.create.assert_awaited_once_with(mock_anomaly)
    features_repo.create.assert_awaited_once_with(mock_features)
