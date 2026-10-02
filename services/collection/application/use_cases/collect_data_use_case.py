from ..dto import CollectDataInput, CollectDataOutput
from ..exceptions import NotFoundError
from ...domain.value_objects import MACAddress, TelemetryWindow, Geoposition
from ...domain.interfaces import ITransaction, IEventPublisher


class CollectDataUseCase:
    def __init__(self, transaction: ITransaction, publisher: IEventPublisher):
        self._transaction = transaction
        self._publisher = publisher

    async def execute(self, input: CollectDataInput) -> CollectDataOutput:
        async with self._transaction as tx:
            mac_addr = MACAddress(value=input.device_mac)
            device = await tx.device.get_by_mac(mac_address=mac_addr.value)

            if not device:
                raise NotFoundError(
                    f"Device {input.device_name} with MAC address {input.device_mac} not found"
                )

            device.collect_telemetry(
                TelemetryWindow(
                    geoposition=Geoposition(
                        latitude=input.latitude, longitude=input.longitude
                    ),
                    timestamp_start=input.timestamp_start,
                    sample_rate=input.sample_rate,
                    speed_rate=input.speed_rate,
                    speed=input.speed,
                    accel_x=input.accel_x,
                    accel_y=input.accel_y,
                    accel_z=input.accel_z,
                    gyro_x=input.gyro_x,
                    gyro_y=input.gyro_y,
                    gyro_z=input.gyro_z,
                    vibration_adc=input.vibration_adc,
                )
            )

        for event in device.pop_events():
            await self._publisher.publish(event)

        return CollectDataOutput(success=True)
