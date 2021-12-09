from typing import TypeVar, Generic

Injected = TypeVar("Injected")

class Injectable(Generic[Injected]):
    pass
