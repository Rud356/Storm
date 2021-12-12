import re
from typing import (
    Union, Type, TypeVar,
    Generic, NamedTuple, Protocol,
    overload
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

HandlerType = TypeVar("HandlerType", bound=StormBaseHandler)


class MatchedHandler(NamedTuple, Generic[HandlerType]):
    handler: Type[HandlerType]
    arguments: re.Match


class RegexRule(Protocol):
    def __init__(self, handler: Type[HandlerType]):
        self.handler = handler
        self.url_regex = handler.url_regex
        self.is_static = handler.is_static_url

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
