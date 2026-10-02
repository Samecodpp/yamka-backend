import grpc

from ...application.dto.input import ClassifyAnomalyInput
from ...application.use_cases.classify_anomaly_use_case import ClassifyAnomalyUseCase
from ...infrastructure.core.grpc import classification_pb2, classification_pb2_grpc


class AnomalyClassificationServicer(
    classification_pb2_grpc.AnomalyClassificationServiceServicer
):

    def __init__(self, use_case: ClassifyAnomalyUseCase) -> None:
        self._use_case = use_case

    def Classify(
        self,
        request: classification_pb2.ClassifyRequest,
        context: grpc.ServicerContext,
    ) -> classification_pb2.ClassifyResponse:
        input_dto = ClassifyAnomalyInput(features=dict(request.features))
        output = self._use_case.execute(input_dto)
        return classification_pb2.ClassifyResponse(
            anomaly_class=output.anomaly_class,
            confidence=output.confidence,
            metadata=output.metadata,
        )
