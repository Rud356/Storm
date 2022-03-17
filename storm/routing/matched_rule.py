from typing import NamedTuple, Type

from storm.requests.handler import HandlerProtocol


class MatchedRule(NamedTuple):
    """
    This class helps packing information about which arguments were parsed
    from url for associated handler to cast values and pass them further.
    """
    handler: Type[HandlerProtocol]
    parsed_arguments: dict[str, str]
