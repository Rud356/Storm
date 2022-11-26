from typing import Union, Optional
from typing import get_args, get_origin, Any, Type

from storm.requests.parameters.parsing.param_specs import ParamSpecs
from storm.requests.parameters.protocol import Parameter


def parse_parameter_type_hint(parameter: Any) -> Type:
    """
    This function helps parsing parameters and validate that they got
    the final type that can not be Optional or other thing that can't be
    directly used for type casting.

    :param parameter: some type hint, that is most likely Parameter subclass.
    :return: type that supplied to Parameter as argument.
    :raises ValueError: raised if you supplied something like int or str, and
        other types that don't have type hints args. Also can be raised if
        you supplied None as parameter or some Union.
    :raises TypeError: if supplied type hint isn't Parameter subclass.
    """
    args: tuple[Any, ...] = get_args(parameter)
    # Making sure it is Parameter type hint
    origin: Optional[Any] = get_origin(parameter)
    if origin is None:
        raise ValueError(
            "Supplied type hint must not have no "
            "origin (be plain type like int, str. etc.)"
        )

    if not issubclass(origin, Parameter):
        raise TypeError(
            f"Parameter type type hint is "
            f"expected, get: {type(get_origin(parameter))}"
        )

    # We make sure we got only 1 type supplied and it's not union or None
    if (
        len(args) != 1 or
        type(None) in args or
        get_origin(args[0]) == Union
    ):
        raise ValueError(
            "Annotation of any parameter must be one concrete type "
            "and None isn't allowed"
        )

    # Returning single one parameter we have
    return args[0]


def parameter_information_from_typehint(
    parameter_name: str,
    type_hint: Any
) -> ParamSpecs:
    """
    This function helps to parse any parameters information based on type hints,
    and it can be used to create url parameters easily, because to what type
    something needs to be cast is figured out.
    :param parameter_name: name of parameter.
    :param type_hint: the associated type hint.
    :return: ParamSpecs instance that has info about type hint.
    :raises TypeError: if supplied type hint is Union that doesn't represent
        Optional.
    :raises ValueError: if type hint is of Optional type, but inside it
        Parameter[type] is not present.
    """
    is_optional: bool = False
    args: tuple[Any, ...] = get_args(type_hint)
    resulting_type: Any = type_hint

    # Order of checks matters, cause first off - issubclass won't work out
    # if we got Union, aka Optional[Parameter[type]] for example.
    if get_origin(type_hint) == Union:
        # We throw error if it's definitely not Optional type hint.
        if type(None) not in args or len(args) != 2:
            raise TypeError(
                "Type hint must only be"
                " Union[Parameter[type], None], Optional[Parameter[type]] "
                "and Parameter[type]"
            )

        # We are sure, so we set is_optional flag to True
        is_optional = True
        # Removing all None values and check that we still have at least 1
        # and then throw it into parse_parameter_type_hint cause it should be
        # it.
        not_none_arguments = [arg for arg in args if arg is not None]
        if len(not_none_arguments) == 0:
            raise ValueError(
                "Type hint must contain at least 1 not None value "
                "to be considered parameter of handler."
            )
        resulting_type: type = parse_parameter_type_hint(
            not_none_arguments[0]
        )

    # TODO: assert that isn't union for mypy
    elif issubclass(get_origin(resulting_type), Parameter):
        # Here is just straightforward parsing of parameter.
        resulting_type = parse_parameter_type_hint(resulting_type)

    else:
        # This thing shouldn't support anything else.
        raise TypeError("Unsupported type hint provided")

    return ParamSpecs(resulting_type, parameter_name, is_optional)
