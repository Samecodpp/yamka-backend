import asyncio
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

from services.collection.application.use_cases.collect_data_use_case import (
    CollectDataUseCase,
)
from services.collection.application.dto.input import CollectDataInput
from services.collection.domain.entities.device import Device
from services.collection.domain.value_objects.mac_addr import MACAddress


class _MockTransaction:
    """Async context manager that exposes a mock device repository."""

    def __init__(self, device_repo: MagicMock) -> None:
        self.device = device_repo

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        pass


def test_collect_data_returns_success():
    mac = "AA:BB:CC:DD:EE:FF"
    device = Device(name="test-device", mac=MACAddress(value=mac), id=uuid4())

    device_repo = MagicMock()
    device_repo.get_by_mac = AsyncMock(return_value=device)

    transaction = _MockTransaction(device_repo=device_repo)

    publisher = MagicMock()
    publisher.publish = AsyncMock()

    use_case = CollectDataUseCase(transaction=transaction, publisher=publisher)

    input_dto = CollectDataInput(
        device_mac=mac,
        device_name="test-device",
        latitude=50.45,
        longitude=30.52,
        speed_rate=10,
        sample_rate=100,
        timestamp_start=datetime.now(timezone.utc),
        speed=[1.0, 2.0, 3.0],
        accel_x=[0.1, 0.2, 0.3],
        accel_y=[0.0, 0.1, 0.0],
        accel_z=[9.8, 9.7, 9.9],
        gyro_x=[0.01, 0.02, 0.01],
        gyro_y=[0.00, 0.01, 0.00],
        gyro_z=[0.00, 0.00, 0.01],
        vibration_adc=[100.0, 120.0, 110.0],
    )

    async def _run():
        return await use_case.execute(input_dto)

    output = asyncio.run(_run())

    assert output.success is True
    device_repo.get_by_mac.assert_awaited_once_with(mac_address=mac)
    publisher.publish.assert_awaited_once()
