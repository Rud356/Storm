from typing import Protocol, runtime_checkable

from storm.types.scope import ASGIConnectionScope
from .rule_protocol import MatchedRule


@runtime_checkable
class Router(Protocol):
    def find_handler(self, scope: ASGIConnectionScope) -> MatchedRule:
        """
        This method finds matching rule from all known rules for that specific
        router and returns MatcherRule instance.

        :param scope: connection parameters from request.
        :return: instance of Matched rule, containing handler class and
            parsed arguments from url as dict.
        """
        pass
