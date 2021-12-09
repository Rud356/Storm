from dataclasses import dataclass
from typing import Any, Type, Optional, get_origin, get_args, Union


@dataclass
class ParameterProperties:
    """
    Class for storing properties of some request parameter.
    """
    is_optional: bool
    casted_to_type: Type
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


def get_original_type_from_optional(unions_args: tuple[Any, Any]) -> Any:
    """
    Returns first value from union args that is not None.
    :param unions_args: arguments from union.
    :return:
    """
    if unions_args[0] is not None:
        return unions_args[0]

    else:
        return unions_args[1]


def parse_parameter_typehint(
    request_parameter_type_hint: tuple[Any, ...]
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
    if len(request_parameter_type_hint) == 1:
        is_optional: bool = False
        casted_to_type: Type = request_parameter_type_hint[0]

        if get_origin(casted_to_type) == Union:
            union_args: tuple[Any, ...] = get_args(casted_to_type)
            if not is_union_representing_optional(union_args):
                raise TypeError(
                    "Only Optional with specific type or Union[type, None]"
                    " are allowed for type hint."
                )

            else:
                is_optional = True
                casted_to_type: tuple[Any, Any]
                casted_to_type: Type = get_original_type_from_optional(
                    casted_to_type
                )

        return ParameterProperties(
            is_optional=is_optional,
            casted_to_type=casted_to_type
        )

    else:
        raise ValueError(
            "Request parameters subclasses can"
            " have exactly type passed to typehint"
            f"(got {len(request_parameter_type_hint)})"
        )
