from __future__ import annotations

import re
from typing import (
    Union, Type, TypeVar, Any,
    Generic, NamedTuple, overload
)

from storm.asgi_data_types.scope import (
    HttpASGIConnectionScope,
    WebSocketASGIConnectionScope
)
from storm.request_handlers import (
    HttpHandler,
    WebSocketHandler,
    StormBaseHandler
)
from .routing_exceptions import NotMatchingRule

HandlerType = TypeVar("HandlerType", bound=Type[StormBaseHandler])


class MatchedHandler(Generic[HandlerType]):
    handler: HandlerType
    arguments: re.Match

    def __init__(self, handler: HandlerType, arguments: re.Match):
        self.handler = handler
        self.arguments = arguments


class RegexRule(Generic[HandlerType]):
    """
    Class that is used internally to find if handler known to this
    rule is one that been asked for.
    """
    def __init__(self, handler: Type[HandlerType], url: str):
        self.handler: Type[HandlerType] = handler
        self.url_regex: re.Pattern = handler._compile_url_regex(  # noqa:
            # this is internal stuff, but we don't need end users to see it
            handler, url
        )
        self.is_static: bool = handler.is_static_url

    @overload
    def match(
        self,
        scope: HttpASGIConnectionScope
    ) -> MatchedHandler[Type[HttpHandler]]:
        pass

    @overload
    def match(
        self,
        scope: WebSocketASGIConnectionScope
    ) -> MatchedHandler[Type[WebSocketHandler]]:
        pass

    def match(
        self,
        scope: Union[HttpASGIConnectionScope, WebSocketASGIConnectionScope]
    ) -> Union[
        MatchedHandler[Type[HttpHandler]],
        MatchedHandler[Type[WebSocketHandler]]
    ]:
        """
        Checks if scope matches some custom rules.

        :param scope: asgi connection scope instance.
        :return: matching request handler.
        :raises NotMatchingRule: if regex doesn't match one in rule.
        """
        url_parameters = self.url_regex.fullmatch(scope.path)
        if url_parameters is None:
            raise NotMatchingRule()

        return MatchedHandler(self.handler, url_parameters)

    def __eq__(self, other: Any) -> bool:
        if issubclass(type(other), RegexRule):
            return other.url_regex == self.url_regex

        else:
            raise ValueError(f"Can not compare RegexRule instance and {other}")
