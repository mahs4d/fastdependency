import pytest
from fastdependency.exceptions import UnResolvableDependencyError
from fastdependency.resolvables import FunctionBasedResolvable


def test_function_based_resolvable() -> None:
    resolvable = FunctionBasedResolvable(lambda: "b")
    assert resolvable.resolve() == "b"


def test_function_based_resolvable_with_method() -> None:
    resolvable = FunctionBasedResolvable(lambda: "a")
    assert resolvable.resolve() == "a"


def test_function_based_resolvable_error() -> None:
    def dep_exc() -> str:
        raise Exception("something went wrong!")

    with pytest.raises(UnResolvableDependencyError):
        FunctionBasedResolvable(dep_exc).resolve()
