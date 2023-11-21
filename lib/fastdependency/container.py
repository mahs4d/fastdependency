from __future__ import annotations


class Container:
    """Base class for all containers."""

    _default_container: Container | None = None

    @classmethod
    def get_default_container(cls) -> Container:
        """Get the default container."""
        if cls._default_container is None:
            raise
        return cls._default_container

    @classmethod
    def set_default_container(cls, container: Container) -> None:
        """Set the default container."""
        cls._default_container = container

    @classmethod
    def unset_default_container(cls) -> None:
        """Unset the default container."""
        cls._default_container = None
