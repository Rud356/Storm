from abc import ABC, abstractmethod
from typing import Callable, Awaitable

from .asgi_scope import HttpASGIConnectionScope, WebSocketASGIConnectionScope
from .asgi_supported_types import ASGI_SUPPORTED_TYPES


class ASGIApp(ABC):
    """
    Base ASGI app that has minimal functionality to separate http
    and websockets requests.
    """
    async def __call__(
        self, scope: dict,
        receive: Callable[
            [],
            Awaitable[ASGI_SUPPORTED_TYPES]
        ],
        send: Callable[
            [ASGI_SUPPORTED_TYPES],
            Awaitable[ASGI_SUPPORTED_TYPES]
        ]
    ) -> None:
        """
        Method that dispatches if this connection must be handled
        as http or as websocket connection.

        :param scope: dictionary with ASGI scope values.
        :param receive: function that is used to receive ASGI server events
            as dicts.
        :param send: function that is used to respond on received ASGI events.
        :return: nothing.

        :raises RuntimeError: if connection type is not http or websocket.
        """

        connection_type: str = scope["type"]
        if connection_type == "http":
            scope = HttpASGIConnectionScope(**scope)
            await self.http_asgi_app(scope, receive, send)

        elif connection_type == "websocket":
            scope = WebSocketASGIConnectionScope(**scope)
            await self.websocket_asgi_app(scope, receive, send)

        else:
            # Something must've gone very wrong on asgi server side
            raise RuntimeError(
                f"Received connection type is {connection_type}"
                " while must be only http or websocket."
            )

    @abstractmethod
    async def http_asgi_app(
        self, scope: HttpASGIConnectionScope,
        receive: Callable[
            [],
            Awaitable[ASGI_SUPPORTED_TYPES]
        ],
        send: Callable[
            [ASGI_SUPPORTED_TYPES],
            Awaitable[ASGI_SUPPORTED_TYPES]
        ]
    ) -> None:
        """
        Method that handles request as http request.

        :param scope: concrete dataclass instance with connection scope.
        :param receive: function that is used to receive ASGI server events
            as dicts.
        :param send: function that is used to respond on received ASGI events.
        :return: nothing.
        """
        pass

    @abstractmethod
    async def websocket_asgi_app(
        self, scope: WebSocketASGIConnectionScope,
        receive: Callable[
            [],
            Awaitable[ASGI_SUPPORTED_TYPES]
        ],
        send: Callable[
            [ASGI_SUPPORTED_TYPES],
            Awaitable[ASGI_SUPPORTED_TYPES]
        ]
    ) -> None:
        """
        Method that handles request as websocket request.

        :param scope: concrete dataclass instance with connection scope.
        :param receive: function that is used to receive ASGI server events
            as dicts.
        :param send: function that is used to respond on received ASGI events.
        :return: nothing.
        """
        pass
