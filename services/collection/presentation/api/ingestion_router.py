from typing import Annotated
from fastapi import APIRouter, Depends, status

from ..schemas import IngestTelemetriesRequest, IngestTelemetriesResponse
from ..dependencies import get_collect_data_use_case as collect_use_case
from ...application.use_cases.collect_data_use_case import CollectDataUseCase
from ...application.dto import CollectDataInput


router = APIRouter(prefix="/api", tags=["api"])


@router.post(
    "/ingest",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=IngestTelemetriesResponse
)
async def collect_telemetries(
    request: IngestTelemetriesRequest,
    use_case: Annotated[CollectDataUseCase, Depends(collect_use_case)]
):
    output = await use_case.execute(
        CollectDataInput(
            device_name=request.device_name,
            device_mac=request.device_mac,
            latitude=request.latitude,
            longitude=request.longitude,
            speed_rate=request.speed_rate,
            sample_rate=request.sample_rate,
            timestamp_start=request.timestamp_start,
            speed=request.speed,
            accel_x=request.accel_x,
            accel_y=request.accel_y,
            accel_z=request.accel_z,
            gyro_x=request.gyro_x,
            gyro_y=request.gyro_y,
            gyro_z=request.gyro_z,
            vibration_adc=request.vibration_adc
        )
    )

    return IngestTelemetriesResponse(
        message=output.message
    )
