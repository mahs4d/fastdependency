import pytest
from fastdependency.container import Container


@pytest.fixture(name="container")
def fixture_container() -> Container:
    return Container()


def test_set_default_container(container: Container) -> None:
    assert Container.get_default_container() is None
    Container.set_default_container(container=container)
    assert Container.get_default_container() == container


def test_unset_default_container(container: Container) -> None:
    Container.set_default_container(container=container)
    assert Container.get_default_container() == container
    Container.unset_default_container()
    assert Container.get_default_container() is None
