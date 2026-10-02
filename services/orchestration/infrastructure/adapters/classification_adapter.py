from uuid import UUID
import grpc

from ..core.grpc import classification_pb2, classification_pb2_grpc
from ...domain.interfaces import IClassificationPort
from ...domain.entities import Anomaly, Features
from ...domain.value_objects import AnomalyClass


class ClassificationAdapter(IClassificationPort):

    def __init__(self, host: str):
        channel = grpc.aio.insecure_channel(host)
        self._stub = classification_pb2_grpc.AnomalyClassificationServiceStub(
            channel=channel
        )

    async def classify(self, anomaly: Anomaly, features: Features) -> Anomaly:
        accel_features = {
            name.value: features.values[name] for name in Features.acc_feature_names()
        }

        response = await self._stub.Classify(
            classification_pb2.ClassifyRequest(features=accel_features)
        )

        return anomaly.classify(
            anomaly_class=AnomalyClass.from_class_index(response.anomaly_class),
            classification_confidence=response.confidence,
            metadata_key="classification",
            metadata=dict(response.metadata),
        )
