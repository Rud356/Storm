import re
from typing import Type
from storm.requests.handler import HandlerProtocol
from storm.routing.matched_rule import MatchedRule
from storm.types.scope import ASGIConnectionScope
from storm.routing.protocols import Rule
from storm.routing.exceptions import NotMatchingRule


class RegexRule(Rule):
    def __init__(self, url: str, handler: Type[HandlerProtocol]):
        self.url = url
        self.regex = re.compile(url)
        self.associated_handler = handler

    def match(self, scope: ASGIConnectionScope) -> MatchedRule:
        url_parameters = self.regex.fullmatch(scope.path)
        if not url_parameters:
            raise NotMatchingRule("Supplied scope doesn't matches rule")

        return MatchedRule(
            self.associated_handler,
            url_parameters.groupdict()
        )
