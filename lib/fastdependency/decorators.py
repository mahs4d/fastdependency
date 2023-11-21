import inspect
from asyncio import iscoroutinefunction
from functools import lru_cache, wraps
from typing import Callable, Generator, ParamSpec, TypeVar, Awaitable, Coroutine

from fastdependency.container import Container
from fastdependency.resolvables import Resolvable

singleton = lru_cache


def inject(fn):
    """Inject dependencies into functions and methods."""

    def get_arguments(
        container: Container,
        args: tuple,
        kwargs: dict,
    ) -> tuple[Generator, dict]:
        sig_args = inspect.signature(fn).bind(*args, **kwargs)
        sig_args.apply_defaults()
        new_args = (arg.resolve(container=container) if isinstance(arg, Resolvable) else arg for arg in sig_args.args)
        new_kwargs = {
            key: arg.resolve(container=container) if isinstance(arg, Resolvable) else arg
            for key, arg in sig_args.kwargs.items()
        }
        return new_args, new_kwargs

    @wraps(fn)
    def sync_wrapper(*args, **kwargs):
        new_args, new_kwargs = get_arguments(
            container=Container.get_default_container(),
            args=args,
            kwargs=kwargs,
        )
        return fn(*new_args, **new_kwargs)

    @wraps(fn)
    async def async_wrapper(*args, **kwargs):
        new_args, new_kwargs = get_arguments(
            container=Container.get_default_container(),
            args=args,
            kwargs=kwargs,
        )
        return await fn(*new_args, **new_kwargs)

    if iscoroutinefunction(fn):
        return async_wrapper

    return sync_wrapper
