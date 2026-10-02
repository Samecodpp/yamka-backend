import grpc

from ...application.dto.input import DetectAnomalyInput
from ...application.use_cases.detect_anomaly_use_case import DetectAnomalyUseCase
from ...infrastructure.core.grpc import detection_pb2, detection_pb2_grpc


class AnomalyDetectionServicer(detection_pb2_grpc.AnomalyDetectionServiceServicer):

    def __init__(self, use_case: DetectAnomalyUseCase) -> None:
        self._use_case = use_case

    def Detect(
        self,
        request: detection_pb2.DetectRequest,
        context: grpc.ServicerContext,
    ) -> detection_pb2.DetectResponse:
        input_dto = DetectAnomalyInput(features=dict(request.features))
        output = self._use_case.execute(input_dto)
        return detection_pb2.DetectResponse(
            is_anomaly=output.is_anomaly,
            confidence=output.confidence,
            metadata=output.metadata,
        )
