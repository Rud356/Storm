from abc import ABC, abstractmethod

from .asgi_scope import HttpASGIConnectionScope, WebSocketASGIConnectionScope


class ASGIApp(ABC):
    async def __call__(self, scope: dict, receive, send) -> None:
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
        self, scope: HttpASGIConnectionScope, receive, send
    ) -> None:
        pass

    @abstractmethod
    async def websocket_asgi_app(
        self, scope: WebSocketASGIConnectionScope, receive, send
    ) -> None:
        pass
