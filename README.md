# Fast Dependency

## Installation

`pip install fastdependency`

## Usage

```python
from fastdependency import Depends, inject


def username() -> str:
    return 'mahdi'


def password() -> str:
    return '123***456'


@inject
def my_function(
        param: int,
        username: str = Depends(username),  # Gets it from function.
        password: str = Depends(password),  # Gets it from container.
):
    print(param)
    print(username)
    print(password)


my_function(12)
```

## TODO
- [ ] Full Docs
- [ ] Precommit