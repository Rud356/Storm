from datetime import datetime, date, time
from pathlib import Path
from typing import Type, Protocol, runtime_checkable
from uuid import UUID

from .base_request_parameter import BaseRequestParameter


@runtime_checkable
class CompilableUrlParameter(Protocol):
    """
    Protocol for unsupported by default types.
    """

    @staticmethod
    def __compile_to_regex__() -> str:
        """
        Returns a regex that will give a string that type can be loaded from.
        :return: regex string.
        """
        pass


class URLParameter(BaseRequestParameter):
    """
    Class that is used to represent url parameters as handlers attribute.
    All names of parameters will be matched to groups names, specified in
    url as <name>. For example /api/<version>. They must always exist and
    it's forbidden to type hint them as optional.
    Examples:

    .. code-block:: python

        class A(StormBaseHandler, url="/api/<version>"):
            version: UrlParameter[int]

            def get(self):
                print(self.version)  # int
    """


def compile_type_to_regex(
    type_to_compile: type
) -> str:
    """
    Compiles some type into a regex, that will represent it in url,
    and later will be used to unpack url params. Be default following types
    are supported: int, bool, float, str, Path, datetime, date, time, UUID.
    You can add custom types by implementing CompilableUrlParameter protocol.

    :param type_to_compile: some type.
    :return: regex as string.
    :raises TypeError: if type isn't one of default supported and
        it doesn't implements CompilableUrlParameter protocol
    """
    if issubclass(type_to_compile, CompilableUrlParameter):
        return type_to_compile.__compile_to_regex__()

    elif issubclass(
        type_to_compile, int
    ) and not issubclass(type_to_compile, bool):
        return r"-\d+|\d+"

    elif issubclass(type_to_compile, float):
        return r"[-+]?\d*\.\d+|\d+"

    elif issubclass(type_to_compile, str):
        return r"\w+"

    elif issubclass(type_to_compile, Path):
        return r".+"

    elif issubclass(type_to_compile, (datetime, date, time)):
        return "(.*?)"

    elif issubclass(type_to_compile, UUID):
        # Taken from: https://gist.github.com/kgriffs/c20084db6686fee2b363fdc1a8998792
        return r"[a-f0-9]{8}-[a-f0-9]{4}-[1-5][a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12}"

    else:
        raise TypeError(
            f"Unsupported type {type_to_compile}. "
            f"Please, inherit from this type and CompilableUrlParameter "
            f"and implement method __compile_to_regex__."
        )


def compile_type_to_named_group(
    name: str,
    type_to_compile: Type
) -> str:
    """
    Function that compiles type to a named group in regex.

    :param name: future group name. Must be a valid python identifier.
    :param type_to_compile: type that will be compiled into regex.
    :return: regex string that contains a named group.
    :raises ValueError: if group name is invalid.
    """
    if not name.isidentifier():
        raise ValueError(
            f"Group name can not be {name}, because they "
            f"must be valid python variable identifiers"
        )

    type_regex = compile_type_to_regex(type_to_compile)
    group_regex = r"(?P<%s>%s)" % (name, type_regex)
    return group_regex
