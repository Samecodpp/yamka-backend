from dataclasses import dataclass

@dataclass(frozen=True)
class CollectDataOutput:
    success: bool
    message: str | None = None
