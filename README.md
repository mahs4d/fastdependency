# Fast Dependency

## Installation

`pip install fastdependency`

## Usage

```python
from fastdependency import Container, Depends


# Define your default global container class.
class MyContainer(Container):
    def lock_password(self) -> str:
        return "123**456"


# Create an instance of your container and set it as default.
Container.set_default_container(MyContainer())


def username() -> str:
    return 'mahdi'


def my_function(
        param: int,
        username=Depends(username),  # Gets it from function.
        password=Depends('lock_password'),  # Gets it from container.
):
    print(param)
    print(username)
    print(password)


my_function(12)
```

## TODO
- [ ] Docs
- [ ] Support `Annotated` type-hint injection
