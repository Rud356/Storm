from typing import NamedTuple, Type


class ParamSpecs(NamedTuple):
    """
    Class that stores information about parameters.
    """
    parameter_type: Type
    parameter_name: str
    is_optional: bool = False

