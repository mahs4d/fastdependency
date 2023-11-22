from abc import ABC, abstractmethod
from typing import Any, Callable, override

from fastdependency.exceptions import UnResolvableDependencyError


class Resolvable(ABC):
    """Base class for all resolvables."""

    @abstractmethod
    def resolve(self) -> Any:
        """Resolve the dependency and return it."""


class FunctionBasedResolvable(Resolvable):
    """Resolvable that uses input function to get the dependency."""

    def __init__(self, dep_fn: Callable[..., Any]):
        self.dep_fn = dep_fn

    @override
    def resolve(self) -> Any:
        try:
            return self.dep_fn()
        except Exception as ex:
            raise UnResolvableDependencyError from ex
