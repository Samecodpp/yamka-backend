from typing import TypeVar, Generic
from abc import ABC, abstractmethod

In = TypeVar("In")
Out = TypeVar("Out")


class IStep(ABC, Generic[In, Out]):

    @abstractmethod
    def fit(self, X: In, y=None) -> "IStep[In, Out]": ...

    @abstractmethod
    def transform(self, X: In) -> Out: ...

    def fit_transform(self, X: In, y=None) -> Out:
        return self.fit(X, y).transform(X)
