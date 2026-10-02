from enum import Enum


class AnomalyClass(str, Enum):
    POTHOLE = "pothole"
    BUMP = "bump"

    @classmethod
    def from_class_index(cls, index: int) -> "AnomalyClass":
        members = list(cls)
        if index < 0 or index >= len(members):
            raise ValueError(f"Invalid class index: {index}")
        return members[index]
