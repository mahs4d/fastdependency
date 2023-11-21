from typing import Any, Callable

from fastdependency.exceptions import UnResolvableDependencyError
from fastdependency.resolvables import (
    FunctionBasedResolvable,
    NameBasedResolvable,
    Resolvable,
)


def Depends(x: Callable[..., Any] | str) -> Resolvable:
    """Function for generating resolvables which is also compatible with FastAPI."""

    if callable(x):
        return FunctionBasedResolvable(x)

    if isinstance(x, str):
        return NameBasedResolvable(x)

    raise UnResolvableDependencyError(
        "Only dep_name and functions are allowed in `Depends`!",
    )
