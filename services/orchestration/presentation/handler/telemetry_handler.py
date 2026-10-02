import logging

from ...application.dto.input import ProcessTelemetryInput
from ...application.use_cases.processing_telemetry_use_case import (
    ProcessingTelemetryUseCase,
)

logger = logging.getLogger(__name__)


def make_telemetry_handler(use_case: ProcessingTelemetryUseCase):
    async def handler(data: dict) -> None:
        try:
            input_dto = ProcessTelemetryInput.from_event(data)
        except (KeyError, ValueError) as exc:
            logger.error("Failed to parse telemetry event: %s", exc)
            return

        output = await use_case.execute(input_dto)
        if output.is_anomaly:
            logger.info(
                "ANOMALY detected | device=%s | class=%s | conf=%.4f | id=%s",
                output.device_id,
                output.anomaly_class.value if output.anomaly_class else "unknown",
                output.detection_confidence,
                output.anomaly_id,
            )
        else:
            logger.info(
                "OK              | device=%s | conf=%.4f",
                output.device_id,
                output.detection_confidence,
            )

    return handler
