from typing import Any, Callable

from fastdependency.exceptions import UnResolvableDependencyError
from fastdependency.resolvables import (
    FunctionBasedResolvable,
    Resolvable,
)


def Depends(x: Callable[..., Any] | str) -> Resolvable:
    """Utility function for creating resolvables based on input."""

    if callable(x):
        return FunctionBasedResolvable(x)

    raise UnResolvableDependencyError(
        "Only dep_name and functions are allowed in `Depends`!",
    )
