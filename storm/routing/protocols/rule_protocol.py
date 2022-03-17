from typing import Protocol, runtime_checkable, Type

from storm.requests.handlers import HandlerProtocol
from storm.routing.matched_rule import MatchedRule
from storm.types.scope import ASGIConnectionScope


@runtime_checkable
class Rule(Protocol):
    url: str
    associated_handler: Type[HandlerProtocol]

    def match(self, scope: ASGIConnectionScope) -> MatchedRule:
        """
        Method to check if scope is matching requirements.
        :param scope: received connection properties.
        :return: MatchedRule instance if does match.
        :raises NotMatchingRule: if scope doesn't match.
        """
        pass
