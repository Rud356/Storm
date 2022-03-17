from __future__ import annotations

from abc import ABC
from typing import Any, Generic, TypeVar

ParamType = TypeVar("ParamType")


class Parameter(ABC, Generic[ParamType]):
    """
    Some parameters of request can be expressed with this protocol.
    """
    def __init__(self, parameter: ParamType):
        self.parameter: ParamType = parameter

    def __get__(self, instance: Any, owner: Any) -> ParamType:
        return self.parameter
