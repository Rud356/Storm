from __future__ import annotations
from abc import ABC
from typing import Generic, TypeVar, Any, Type, Optional

ParameterType = TypeVar("ParameterType")

# TODO: write better explanation.


class BaseRequestParameter(ABC, Generic[ParameterType]):
    """
    Base class for parameters that will be initialized to get
    some parameters from preloaded data and then make them
    attributes of class. To cast them to any wanted value you
    should know input type of that specific data place and then you
    make a type hint with class, that can take only one parameter,
    which is going to be our input data, and then create
    already working instance of this class.

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

    @classmethod
    def load_parameter(
        cls, parameter: Any, cast_to_type: Optional[Type[Any]] = None
    ) -> BaseRequestParameter[ParameterType]:
        parameter: ParameterType = cast_to_type(parameter)
        return cls(parameter)
