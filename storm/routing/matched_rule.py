from typing import NamedTuple, Type

from storm.requests.handlers import HandlerProtocol


class MatchedRule(NamedTuple):
    """
    This class helps packing information about which arguments were parsed
    from url for associated handlers to cast values and pass them further.
    """
    handler: Type[HandlerProtocol]
    parsed_arguments: dict[str, str]
