from storm.requests import HttpHandler, WebSocketHandler
from storm.types.scope import ASGIConnectionScope, WebSocketScope, HTTPScope
from .exceptions import (
    UnknownHandlerType, NotMatchingRule, HandlerNotFound,
    UnknownScopeType
)
from .matched_rule import MatchedRule
from .protocols import Router, Rule


class StormRouter(Router):
    ws_rules: list[Rule]
    http_rules: list[Rule]

    def __init__(self):
        self.ws_rules = []
        self.http_rules = []

    def add_rule(self, rule: Rule) -> None:
        """
        Method that adds some rule to lists based on if it's http handler or
        websocket handler.
        :param rule:
        :type rule:
        :return:
        :rtype:
        """
        if isinstance(rule.associated_handler, HttpHandler):
            self.http_rules.append(rule)

        elif isinstance(rule.associated_handler, WebSocketHandler):
            self.ws_rules.append(rule)

        else:
            raise UnknownHandlerType(
                f"Got handler of type {type(rule.associated_handler)}"
            )

    def find_handler(self, scope: ASGIConnectionScope) -> MatchedRule:
        if scope.type == "http":
            assert isinstance(scope, HTTPScope), (
                "Types doesn't match what been passed here (must be HTTPScope)"
                f": got {type(scope)}"
            )
            return self.find_http_handler(scope)

        elif scope.type == "ws":
            assert isinstance(scope, WebSocketScope), (
                "Types doesn't match what been passed here "
                "(must be WebSocketScope)"
                f": got {type(scope)}"
            )
            return self.find_ws_handler(scope)

        else:
            raise UnknownScopeType(
                f"Got connection of type {scope.type}, "
                f"which doesn't have handler"
            )

    def find_http_handler(
        self,
        scope: HTTPScope
    ) -> MatchedRule:
        """
        Looks for http handler that are known for router.
        :param scope: instance of scope.
        :return: MatchedHandler instance.
        :raises HandlerNotFound: if didn't found any handler inside of
            router.
        """
        for rule in self.http_rules:
            try:
                return rule.match(scope)

            except NotMatchingRule:
                continue

        else:
            raise HandlerNotFound()

    def find_ws_handler(
        self,
        scope: WebSocketScope
    ) -> MatchedRule:
        """
        Looks for websocket handler that are known for router.
        :param scope: instance of scope.
        :return: MatchedHandler instance.
        :raises HandlerNotFound: if didn't found any handler inside of
            router.
        """
        for rule in self.ws_rules:
            try:
                return rule.match(scope)

            except NotMatchingRule:
                continue

        else:
            raise HandlerNotFound()
