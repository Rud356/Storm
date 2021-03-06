from abc import ABC, abstractmethod
from typing import Callable, Awaitable

from .scope import (
    HttpASGIConnectionScope,
    WebSocketASGIConnectionScope,
    LifetimeASGIScope
)
from .supported_types import ASGI_SUPPORTED_TYPES

receive_typehint = Callable[
    [],
    Awaitable[ASGI_SUPPORTED_TYPES]
]
send_typehint = Callable[
    [ASGI_SUPPORTED_TYPES],
    Awaitable[ASGI_SUPPORTED_TYPES]
]


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
            http_scope: HttpASGIConnectionScope = HttpASGIConnectionScope(
                **scope
            )
            await self.http_asgi_app(http_scope, receive, send)

        elif connection_type == "websocket":
            ws_scope: WebSocketASGIConnectionScope = WebSocketASGIConnectionScope(
                **scope
            )
            await self.websocket_asgi_app(ws_scope, receive, send)

        elif connection_type == "lifetime":
            lifetime_scope: LifetimeASGIScope = LifetimeASGIScope(**scope)
            await self.lifetime_asgi_app(lifetime_scope, receive, send)

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

    @abstractmethod
    async def lifetime_asgi_app(
        self,
        scope: LifetimeASGIScope,
        receive: Callable[
            [],
            Awaitable[ASGI_SUPPORTED_TYPES]
        ],
        send: Callable[
            [ASGI_SUPPORTED_TYPES],
            Awaitable[ASGI_SUPPORTED_TYPES]
        ]
    ):
        """
        Method that handles request as websocket request.

        :param scope: concrete dataclass instance with connection scope.
        :param receive: function that is used to receive ASGI server events
            as dicts.
        :param send: function that is used to respond on received ASGI events.
        :return: nothing.
        """
