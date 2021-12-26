from dataclasses import dataclass
from inspect import isclass
from typing import (
    Any, Optional,
    get_origin, get_args, Union
)


@dataclass
class ParameterProperties:
    """
    Class for storing properties of some request parameter.
    """
    is_optional: bool
    casted_to_type: Any
    default_value: Optional[Any] = None


def is_union_representing_optional(unions_args: tuple[Any, ...]) -> bool:
    return len(unions_args) == 2 and any(
        # Here we check that we got exactly one None arg, and one not None arg
        # so it is optional type hint.
        (
            (arg is not None for arg in unions_args),
            (arg is None for arg in unions_args)
        )
    )


def get_original_type_from_optional(*args: Any) -> Any:
    """
    Returns first value from union args that is not None.
    :return: some type that is not none in union
    """
    unions_args: tuple[type, ...] = args[:2]
    if unions_args[0] is not None:
        return unions_args[0]

    else:
        return unions_args[1]


def parse_parameter_typehint(
    request_parameter_type_hint: Any
) -> ParameterProperties:
    """
    Prepares ParameterProperties from some specific type hint.

    :param request_parameter_type_hint: parameter type hint that
        will be parsed. This includes figuring out if it's Optional parameter
        or not, and the type that will be used in type casting.
    :return: instance of ParameterProperties.

    :raises ValueError: passed too many arguments to type hint.
    :raises TypeError: type hint isn't representing Optional
        or Union[type, None].
    """

    is_optional: bool = False

    if get_origin(request_parameter_type_hint) == Union:
        union_args: tuple[Any, ...] = get_args(request_parameter_type_hint)
        if not is_union_representing_optional(union_args):
            raise TypeError(
                "Only Optional with specific type or Union[type, None]"
                " are allowed for type hint."
            )

        else:
            is_optional = True
            casted_to_type = get_original_type_from_optional(
                union_args
            )

    elif isclass(request_parameter_type_hint):
        casted_to_type = request_parameter_type_hint

    else:
        raise ValueError(
            "Type hints parsing expects to receive only Optional[type] or "
            "some class, that will be instanced when casting value."
        )

    return ParameterProperties(
        is_optional=is_optional,
        casted_to_type=casted_to_type
    )
