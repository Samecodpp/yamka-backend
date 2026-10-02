from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ...domain.entities import Device
from ...domain.interfaces import IDeviceRepository
from ..models.device import DeviceModel


class DeviceRepository(IDeviceRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_mac(self, mac_address: str) -> Device | None:
        stmt = select(DeviceModel).where(DeviceModel.mac == mac_address)
        model = await self._session.scalar(stmt)
        if not model:
            return None
        return self._to_entity(model)

    def _to_entity(self, model: DeviceModel) -> Device:
        return Device(
            id=model.id,
            name=model.name,
            mac=model.mac,
        )
