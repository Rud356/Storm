from __future__ import annotations

from abc import ABC
from typing import Generic, TypeVar, Any

ParameterType = TypeVar("ParameterType")


class BaseRequestParameter(ABC, Generic[ParameterType]):
    """
    Base class for parameters that will be initialized to get
    some parameters from preloaded data and then make them
    attributes of class.
    Passed type must cast to a valid type via single argument.

    example:
    ```
    class A:
        q: QueryParameter[int]

        def get(self):
            print(type(self.q))  # int
    ```
    """
    def __init__(self, request_parameter: ParameterType):
        self.request_parameter = request_parameter

    def __get__(self, instance: Any, owner: Any) -> ParameterType:
        return self.request_parameter
