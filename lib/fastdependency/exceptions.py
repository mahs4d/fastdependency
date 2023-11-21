class NoDefaultContainerError(Exception):
    """Exception to be raised when default container is not set."""


class UnResolvableDependencyError(Exception):
    """Exception to be raised when dependency could not be resolved."""
