from uuid import UUID
import grpc

from ..core.grpc import detection_pb2, detection_pb2_grpc
from ...domain.interfaces import IDetectionPort
from ...domain.entities import Anomaly, Features


class DetectionAdapter(IDetectionPort):

    def __init__(self, host: str):
        channel = grpc.aio.insecure_channel(host)
        self._stub = detection_pb2_grpc.AnomalyDetectionServiceStub(channel=channel)

    async def detect(self, device_id: UUID, features: Features) -> Anomaly:
        accel_features = {
            name.value: features.values[name] for name in Features.acc_feature_names()
        }

        response = await self._stub.Detect(
            detection_pb2.DetectRequest(features=accel_features)
        )
        anomaly = Anomaly(
            device_id=device_id,
            is_anomaly=response.is_anomaly,
            detection_confidence=response.confidence,
        )
        anomaly.set_metadata("detection", dict(response.metadata))
        return anomaly
