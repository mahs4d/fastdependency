import pytest
from fastdependency.exceptions import UnResolvableDependencyError
from fastdependency.resolvables import FunctionBasedResolvable, NameBasedResolvable
from fastdependency.utils import Depends


def test_depends_with_name() -> None:
    resolvable = Depends("dep_a")
    assert isinstance(resolvable, NameBasedResolvable)
    assert resolvable.dep_name == "dep_a"


def test_depends_with_function() -> None:
    def dep_a() -> None:
        pass

    resolvable = Depends(dep_a)
    assert isinstance(resolvable, FunctionBasedResolvable)
    assert resolvable.dep_fn == dep_a


def test_depends_invalid_input() -> None:
    with pytest.raises(UnResolvableDependencyError):
        Depends(123)  # type: ignore
