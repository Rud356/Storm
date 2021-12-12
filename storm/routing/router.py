from __future__ import annotations

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
from .routing_exceptions import (
    NotMatchingRule,
    HandlerNotFound,
    NotUniqueHandlerUrl
)
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
        scope: WebSocketASGIConnectionScope
    ) -> MatchedHandler[Type[WebSocketHandler]]:
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

    def add_handler(self, handler: Type[StormBaseHandler]) -> None:
        """
        Adds other handler inside of router.

        :param handler: handlers type.
        :return: nothing.
        """
        handler_type = handler
        rule = RegexRule(handler)

        if issubclass(handler_type, HttpHandler):
            if handler_type in self.http_rules:
                raise NotUniqueHandlerUrl()

            self.http_rules.append(rule)

        elif issubclass(handler_type, WebSocketHandler):
            if handler_type in self.ws_rules:
                raise NotUniqueHandlerUrl()

            self.ws_rules.append(rule)

        else:
            raise ValueError(
                f"Passed rule with handler {handler_type} "
                "is not subclass of StormBaseHandler"
            )

    def merge_router(self, another_router: Router) -> None:
        """
        Merges passed router into current one.
        :param another_router: instance of another router.
        :return: nothing.
        """
        for route in another_router.http_rules:
            if route.handler in self.http_rules:
                duplicate_index = self.http_rules.index(route)

                raise NotUniqueHandlerUrl(
                    f"Duplicate url {route.handler.url} has been found "
                    "in handlers:"
                    f" {type(route.handler).__name__} and "
                    f"{type(self.http_rules[duplicate_index]).__name__}"
                )

            else:
                self.http_rules.append(route)

        for route in another_router.ws_rules:
            if route.handler in self.ws_rules:
                duplicate_index = self.ws_rules.index(route)

                raise NotUniqueHandlerUrl(
                    f"Duplicate url {route.handler.url} has been found "
                    "in handlers:"
                    f" {type(route.handler).__name__} and "
                    f"{type(self.ws_rules[duplicate_index]).__name__}"
                )

            else:
                self.ws_rules.append(route)

    def order_routes(self) -> None:
        self.ws_rules.sort(
            key=lambda v: (v.is_static is True, v.handler.url)
        )
        self.http_rules.sort(
            key=lambda v: (v.is_static is True, v.handler.url)
        )
