import pytest
from fastdependency.container import Container
from fastdependency.exceptions import UnResolvableDependencyError
from fastdependency.resolvables import FunctionBasedResolvable, NameBasedResolvable


class StubContainer(Container):
    def dep_a(self) -> str:
        return "a"

    def dep_b(self) -> str:
        return "b"

    def dep_exc(self) -> str:
        raise Exception("something went wrong!")


@pytest.fixture(name="container")
def fixture_container() -> StubContainer:
    return StubContainer()


def dep_c() -> str:
    return "c"


def test_function_based_resolvable(container: StubContainer) -> None:
    resolvable = FunctionBasedResolvable(dep_c)
    assert resolvable.resolve(container=container) == "c"


def test_function_based_resolvable_with_method(container: StubContainer) -> None:
    resolvable = FunctionBasedResolvable(container.dep_a)
    assert resolvable.resolve(container=container) == "a"


def test_function_based_resolvable_error(container: StubContainer) -> None:
    with pytest.raises(UnResolvableDependencyError):
        FunctionBasedResolvable(container.dep_exc).resolve(container=container)


def test_name_based_resolvable(container: StubContainer) -> None:
    resolvable = NameBasedResolvable("dep_b")
    assert resolvable.resolve(container=container) == "b"


def test_name_based_resolvable_not_found(container: StubContainer) -> None:
    with pytest.raises(UnResolvableDependencyError):
        NameBasedResolvable("dep_d").resolve(container=container)


def test_name_based_resolvable_error(container: StubContainer) -> None:
    with pytest.raises(UnResolvableDependencyError):
        NameBasedResolvable("dep_exc").resolve(container=container)
