from abc import ABC, abstractmethod
from typing import Generic, TypeVar

TInput = TypeVar("TInput")
TOutput = TypeVar("TOutput")


class IMapper(ABC, Generic[TInput, TOutput]):
    @abstractmethod
    def map(self, source: TInput) -> TOutput: ...
