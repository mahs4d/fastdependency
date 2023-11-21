from typing import Annotated

import pytest
from fastdependency.container import Container
from fastdependency.decorators import inject, singleton
from fastdependency.resolvables import (
    FunctionBasedResolvable,
    NameBasedResolvable,
    Resolvable,
)


class StubContainer(Container):
    def __init__(self):
        self._i = 0
        self._j = 0

    def dep_a(self) -> str:
        return "a"

    def dep_b(self) -> str:
        return "b"

    @singleton
    def dep_singleton(self) -> int:
        self._i += 1
        return self._i

    def dep_not_singleton(self) -> int:
        self._j += 1
        return self._j


@pytest.fixture(name="container")
def fixture_container() -> StubContainer:
    return StubContainer()


def test_singleton(container: StubContainer) -> None:
    a = FunctionBasedResolvable(container.dep_singleton).resolve(container=container)
    b = FunctionBasedResolvable(container.dep_singleton).resolve(container=container)
    assert a == b


def test_not_singleton(container: StubContainer) -> None:
    a = FunctionBasedResolvable(container.dep_not_singleton).resolve(
        container=container,
    )
    b = FunctionBasedResolvable(container.dep_not_singleton).resolve(
        container=container,
    )
    assert a != b


def test_inject_sync(container: StubContainer) -> None:
    Container.set_default_container(container=container)

    @inject
    def fn(
        x: int,
        y: str = "y",
        a: Annotated[Resolvable, str] = FunctionBasedResolvable(container.dep_a),
        b: Annotated[Resolvable, str] = NameBasedResolvable("dep_b"),
        z: int = 2,
        single1: Annotated[Resolvable, int] = FunctionBasedResolvable(
            container.dep_singleton,
        ),
        single2: Annotated[Resolvable, int] = FunctionBasedResolvable(
            container.dep_singleton,
        ),
    ) -> None:
        assert x == 1
        assert y == "y"
        assert a == "a"
        assert b == "b"
        assert z == 2
        assert single1 == single2

    fn(1)
    fn(x=1, z=2)


async def test_inject_async(container: StubContainer) -> None:
    Container.set_default_container(container=container)

    @inject
    async def fn(
        x: int,
        y: str = "y",
        a: Annotated[Resolvable, str] = FunctionBasedResolvable(container.dep_a),
        b: Annotated[Resolvable, str] = NameBasedResolvable("dep_b"),
        z: int = 2,
        single1: Annotated[Resolvable, int] = FunctionBasedResolvable(
            container.dep_singleton,
        ),
        single2: Annotated[Resolvable, int] = FunctionBasedResolvable(
            container.dep_singleton,
        ),
    ) -> None:
        assert x == 1
        assert y == "y"
        assert a == "a"
        assert b == "b"
        assert z == 2
        assert single1 == single2

    await fn(1)
    await fn(x=1, z=2)


def test_inject_override(container: StubContainer) -> None:
    Container.set_default_container(container=container)

    @inject
    def fn(
        x: int,
        y: str = "y",
        a: Annotated[Resolvable, str] = FunctionBasedResolvable(container.dep_a),
        b: Annotated[Resolvable, str] = NameBasedResolvable("dep_b"),
        z: int = 2,
        single1: Annotated[Resolvable, int] = FunctionBasedResolvable(
            container.dep_singleton,
        ),
        single2: Annotated[Resolvable, int] = FunctionBasedResolvable(
            container.dep_singleton,
        ),
    ) -> None:
        assert x == 1
        assert y == "y"
        assert a == "OVERRIDE"
        assert b == "b"
        assert z == 2
        assert single1 == single2

    fn(1, "y", "OVERRIDE")
    fn(x=1, a="OVERRIDE")


def test_inject_varargs(container: StubContainer) -> None:
    Container.set_default_container(container=container)

    @inject
    def fn(
        *args,
        a: Annotated[Resolvable, str] = FunctionBasedResolvable(container.dep_a),
        b: Annotated[Resolvable, str] = NameBasedResolvable("dep_b"),
        z: int = 2,
        single1: Annotated[Resolvable, int] = FunctionBasedResolvable(container.dep_singleton),
        single2: Annotated[Resolvable, int] = FunctionBasedResolvable(container.dep_singleton),
        **kwargs,
    ) -> None:
        assert args[0] == 1
        assert args[1] == "y"
        assert a == "a"
        assert b == "b"
        assert z == 2
        assert single1 == single2
        assert kwargs == {
            "w": "w",
        }

    fn(1, "y", z=2, w="w")
