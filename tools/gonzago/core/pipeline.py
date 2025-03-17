from abc import abstractmethod
from typing import Protocol, TypeVar

# https://pypyr.io/

# This is all to large for what this is.
# Just use https://rivery.io/data-learning-center/etl-pipeline-python/

T = TypeVar("T")
TIn = TypeVar("TIn")
TOut = TypeVar("TOut")


class Target:
    pass


class Provider[T](Protocol):
    @abstractmethod
    def get(self) -> T:
        raise NotImplementedError


class Validator[T](Protocol):
    @abstractmethod
    def validate(self, item: T) -> bool:
        raise NotImplementedError


class Transformer[TIn, TOut](Protocol):
    @abstractmethod
    def transform(self, item: TIn) -> TOut:
        raise NotImplementedError
