from abc import ABC, abstractmethod
from ..entities import Device


class IDeviceRepository(ABC):

    @abstractmethod
    async def get_by_mac(self, mac_address: str) -> Device | None: ...
