from abc import ABC, abstractmethod
from typing import Any, Callable, override

from fastdependency.container import Container
from fastdependency.exceptions import UnResolvableDependencyError


class Resolvable(ABC):
    """Base class for all resolvables."""

    @abstractmethod
    def resolve(self, container: Container) -> Any:
        """Resolve the dependency and return it."""


class FunctionBasedResolvable(Resolvable):
    """Resolvable that uses input function to get the dependency."""

    def __init__(self, dep_fn: Callable[..., Any]):
        self.dep_fn = dep_fn

    @override
    def resolve(self, container: Container) -> Any:
        try:
            return self.dep_fn()
        except Exception as ex:
            raise UnResolvableDependencyError from ex


class NameBasedResolvable(Resolvable):
    """Resolvable that uses name of the function in container for getting dependency."""

    def __init__(self, dep_name: str):
        self.dep_name = dep_name

    @override
    def resolve(self, container: Container) -> Any:
        try:
            return getattr(container, self.dep_name)()
        except AttributeError as ex:
            raise UnResolvableDependencyError(
                f"Couldn't find `{self.dep_name}` in container",
            ) from ex
        except Exception as ex:
            raise UnResolvableDependencyError from ex
