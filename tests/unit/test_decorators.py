import random

from fastdependency.decorators import inject, singleton
from fastdependency.resolvables import FunctionBasedResolvable


def test_singleton() -> None:
    @singleton
    def dep_singleton() -> int:
        return random.randint(1, 99999999)

    a = FunctionBasedResolvable(dep_singleton).resolve()
    b = FunctionBasedResolvable(dep_singleton).resolve()

    assert a == b


def test_not_singleton() -> None:
    def dep_not_singleton() -> int:
        return random.randint(1, 99999999)

    a = FunctionBasedResolvable(dep_not_singleton).resolve()
    b = FunctionBasedResolvable(dep_not_singleton).resolve()

    assert a != b


def test_inject_sync() -> None:
    @inject
    def fn(
        arg1: int,
        arg2: str = "y",
        dep_a: str = FunctionBasedResolvable(lambda: "a"),
    ) -> None:
        assert arg1 == 1
        assert arg2 == "y"
        assert dep_a == "a"

    fn(1)
    fn(arg1=1)


async def test_inject_async() -> None:
    @inject
    async def fn(
        arg1: int,
        arg2: str = "y",
        dep_a: str = FunctionBasedResolvable(lambda: "a"),
    ) -> None:
        assert arg1 == 1
        assert arg2 == "y"
        assert dep_a == "a"

    await fn(1)
    await fn(arg1=1)


def test_inject_override() -> None:
    @inject
    def fn(
        arg1: int,
        arg2: str = "y",
        dep_a: str = FunctionBasedResolvable(lambda: "a"),
        dep_b: str = FunctionBasedResolvable(lambda: "b"),
    ) -> None:
        assert arg1 == 1
        assert arg2 == "y"
        assert dep_a == "OVERRIDE"
        assert dep_b == "b"

    fn(1, "y", "OVERRIDE")
    fn(arg1=1, dep_a="OVERRIDE")


def test_inject_varargs() -> None:
    @inject
    def fn(
        *args,
        dep_a: str = FunctionBasedResolvable(lambda: "a"),
        dep_b: str = FunctionBasedResolvable(lambda: "b"),
        **kwargs,
    ) -> None:
        assert args[0] == 1
        assert args[1] == "y"
        assert dep_a == "a"
        assert dep_b == "b"
        assert kwargs == {
            "arg3": "z",
        }

    fn(1, "y", arg3="z")
