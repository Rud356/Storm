from typing import Type, Any, Optional

from .request_parameter import BaseRequestParameter, ParameterType


# TODO: write better explanation.

class QueryParameter(BaseRequestParameter):
    """
    Class for treating request query arguments as attributes
    with specific types.
    """

    @classmethod
    def load_parameter(
        cls, parameter: str, cast_to_type: Optional[Type[Any]] = None
    ) -> BaseRequestParameter[ParameterType]:
        parameter: ParameterType = cast_to_type(parameter)
        return cls(parameter)
