from typing import Type

from storm.asgi_data_types.scope import (
    HttpASGIConnectionScope,
    WebSocketASGIConnectionScope
)
from storm.request_handlers import (
    HttpHandler,
    WebSocketHandler,
    StormBaseHandler
)
from .routing_exceptions import NotMatchingRule, HandlerNotFound
from .rule import RegexRule, MatchedHandler


class Router:
    ws_rules: list[RegexRule[WebSocketHandler]]
    http_rules: list[RegexRule[HttpHandler]]

    def __init__(self):
        self.ws_rules = []
        self.http_rules = []

    def find_http_handler(
        self,
        scope: HttpASGIConnectionScope
    ) -> MatchedHandler[Type[HttpHandler]]:
        for rule in self.http_rules:
            try:
                return rule.match(scope)

            except NotMatchingRule:
                continue

        else:
            raise HandlerNotFound()

    def find_ws_handler(
        self,
        scope: WebSocketASGIConnectionScope
    ) -> MatchedHandler[Type[WebSocketHandler]]:
        for rule in self.ws_rules:
            try:
                return rule.match(scope)

            except NotMatchingRule:
                continue

        else:
            raise HandlerNotFound()

    def add_handler(self, handler: Type[StormBaseHandler]) -> None:
        handler_type = handler
        rule = RegexRule(handler)

        if issubclass(handler_type, HttpHandler):
            self.http_rules.append(rule)

        elif issubclass(handler_type, WebSocketHandler):
            self.ws_rules.append(rule)

        else:
            raise ValueError(
                f"Passed rule with handler {handler_type} "
                "is not subclass of StormBaseHandler"
            )
