from concurrent.futures import ThreadPoolExecutor, Executor
from typing import (
    Awaitable, Callable, Generic,
    Mapping, Optional, TypeVar, Union
)

from storm.routing import Router
from storm.types.asgi_app import ASGIApp
from storm.types.asgi_supported_types import ASGI_SUPPORTED_TYPES
from storm.types.scope import HTTPScope, LifespanScope, WebSocketScope
from storm.types.events import EventDispatcher, lifespan
from storm.loggers import events_logger


ConfigInstance = TypeVar("ConfigInstance", bound=Mapping)


class StormApp(ASGIApp, Generic[ConfigInstance]):
    def __init__(
        self,
        router: Router,
        routing_executor: Executor = ThreadPoolExecutor(
            thread_name_prefix="routing_"
        ),
        debug: bool = __debug__,
        name: str = "Storm App",
        host: str = "localhost",
        port: int = 4608,
        config: Optional[ConfigInstance] = None,
    ):
        self.router: Router = router
        self.routing_executor: Executor = routing_executor
        self.debug: bool = debug
        self.name: str = name
        self.host: str = host
        self.port: int = port
        self.config: Optional[ConfigInstance] = config
        self.event_dispatcher: EventDispatcher = EventDispatcher()

    async def __call__(
        self,
        scope: dict,
        receive: Callable[
            [],
            Awaitable[ASGI_SUPPORTED_TYPES]
        ],
        send: Callable[
            [ASGI_SUPPORTED_TYPES],
            Awaitable[ASGI_SUPPORTED_TYPES]
        ]
    ) -> None:
        await super().__call__(scope, receive, send)
        # Log received scope
        events_logger.debug(scope)

        try:
            connection_type: str = scope["type"]

        except KeyError as err:
            raise KeyError(
                "No type was found in scope which should;ve never happened"
            ) from err

        if connection_type == "http":
            http_scope: HTTPScope = HTTPScope(**scope)
            await self.http_connection(http_scope, receive, send)

        elif connection_type == "websocket":
            ws_scope: WebSocketScope = WebSocketScope(**scope)
            await self.ws_connection(ws_scope, receive, send)

        elif connection_type == "lifespan":
            lifespan_scope: LifespanScope = LifespanScope(**scope)
            await self.lifespan_handling(lifespan_scope, receive, send)

        else:
            raise RuntimeError(
                f"Received connection type is {connection_type}"
                " while must be only http or websocket."
            )

    async def http_connection(
        self,
        scope: HTTPScope,
        receive: Callable[
            [],
            Awaitable[ASGI_SUPPORTED_TYPES]
        ],
        send: Callable[
            [ASGI_SUPPORTED_TYPES],
            Awaitable[ASGI_SUPPORTED_TYPES]
        ]
    ) -> None:
        pass

    async def ws_connection(
        self,
        ws_scope: WebSocketScope,
        receive: Callable[
            [],
            Awaitable[ASGI_SUPPORTED_TYPES]
        ],
        send: Callable[
            [ASGI_SUPPORTED_TYPES],
            Awaitable[ASGI_SUPPORTED_TYPES]
        ]
    ) -> None:
        pass

    async def lifespan_handling(
        self,
        lifespan_scope: LifespanScope,  # noqa: this is needed to match
        # signature of ASGI execution methods
        receive: Callable[
            [],
            Awaitable[ASGI_SUPPORTED_TYPES]
        ],
        send: Callable[
            [ASGI_SUPPORTED_TYPES],
            Awaitable[ASGI_SUPPORTED_TYPES]
        ]
    ) -> None:
        event: Union[
            lifespan.Startup,
            lifespan.Shutdown
        ] = self.event_dispatcher.dispatch_event(await receive())

        if isinstance(event, lifespan.Startup):
            events_logger.info("App initialization")

            try:
                await self.on_start()

            except Exception as err:
                events_logger.info("App failed to start", exc_info=err)
                response: lifespan.StartupFailed = lifespan.StartupFailed(
                    message=str(err)
                )
                await send(response.dict())
                raise err

            events_logger.info("Initialization complete")
            await send(lifespan.StartupComplete().dict())

        elif isinstance(event, lifespan.Shutdown):
            events_logger.info("App shutdown begins")

            try:
                await self.on_shutdown()

            except Exception as err:
                events_logger.info("App failed to shut down", exc_info=err)
                response: lifespan.ShutdownFailed = lifespan.ShutdownFailed(
                    message=str(err)
                )
                await send(response.dict())
                raise err

            await send(lifespan.ShutdownComplete().dict())

        else:
            raise RuntimeError(f"Unknown event type: {type(event)}")

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
        pass
