import asyncio
from typing import Generic, TypeVar, Mapping, Optional, Type
from concurrent.futures import ThreadPoolExecutor, Executor

from .asgi_data_types import (
    HttpASGIConnectionScope,
    LifetimeASGIScope,
    WebSocketASGIConnectionScope,
    send_typehint,
    receive_typehint
)
from .request_handlers import HttpHandler
from .asgi_data_types.app import ASGIApp
from .routing import Router, HandlerNotFound


ConfigType = TypeVar("ConfigType", bound=Mapping)


class StormApp(ASGIApp, Generic[ConfigType]):
    def __init__(
        self,
        router: Router,
        routing_executor: Executor = ThreadPoolExecutor(
            thread_name_prefix="routing_"
        ),
        name: str = "Storm App",
        host: str = "localhost",
        config: Optional[ConfigType] = None
    ):
        self.name = name
        self.host = host
        self.config: ConfigType = config
        self.router = router
        self.routing_executor: Executor = routing_executor

        if self.config is None:
            self.config = {}

    async def http_asgi_app(
        self,
        scope: HttpASGIConnectionScope,
        receive: receive_typehint,
        send: send_typehint
    ) -> None:
        try:
            handler: Type[HttpHandler] = await asyncio.get_running_loop(
                ).run_in_executor(
                    self.routing_executor,
                    self.router.find_http_handler,
                    scope
                )

        except HandlerNotFound:
            # TODO: return not found default response
            return

        handler_instance: HttpHandler = handler(
            self, scope, receive
        )
        await handler_instance.execute()

    async def websocket_asgi_app(
        self,
        scope: WebSocketASGIConnectionScope,
        receive: receive_typehint,
        send: send_typehint
    ) -> None:
        pass

    async def lifetime_asgi_app(
        self,
        scope: LifetimeASGIScope,
        receive: receive_typehint,
        send: send_typehint
    ):
        pass

    async def on_start(self) -> None:
        """
        Called when app starts up.

        :return: nothing.
        """
        pass

    async def on_shutdown(self) -> None:
        """
        Called when app stops.

        :return: nothing.
        """
