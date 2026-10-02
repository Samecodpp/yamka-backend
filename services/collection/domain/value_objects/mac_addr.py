from dataclasses import dataclass
import re


@dataclass(frozen=True)
class MACAddress:
    value: str
    _MAC_REGEX = re.compile(
        r"^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$"
    )

    def __post_init__(self):
        normalized = self._normalize(self.value)

        if not self._is_valid(normalized):
            raise ValueError(f"Invalid MAC address: {self.value}")

        object.__setattr__(self, "value", normalized)

    @classmethod
    def _normalize(cls, value: str) -> str:
        value = value.replace("-", ":").upper()
        return value

    @classmethod
    def _is_valid(cls, value: str) -> bool:
        return bool(cls._MAC_REGEX.fullmatch(value))
