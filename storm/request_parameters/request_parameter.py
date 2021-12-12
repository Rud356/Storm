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
    All names of looked up arguments will match the name of arguments, that
    are type hinted with this class subclasses.

    Examples:

    .. code-block:: python

        class A(StormBaseHandler):
            q: QueryParameter[int]

            def get(self):
                print(type(self.q))  # int

    .. code-block:: python

        class A(StormBaseHandler):
            q: QueryParameter[typing.Optional[int]] = 1

            def get(self):
                # If we got no value in query arguments - we will get default
                # as value of 1.
                # If default isn't provided - there will be None.
                print(self.q)  # 1
    """
    def __init__(self, request_parameter: ParameterType):
        self.request_parameter = request_parameter

    def __get__(self, instance: Any, owner: Any) -> ParameterType:
        return self.request_parameter
