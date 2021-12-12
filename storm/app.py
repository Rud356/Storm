import asyncio
from concurrent.futures import ThreadPoolExecutor, Executor
from typing import Generic, TypeVar, Mapping, Optional, Type

from .asgi_data_types import (
    HttpASGIConnectionScope,
    LifetimeASGIScope,
    WebSocketASGIConnectionScope,
    send_typehint,
    receive_typehint,
    events
)
from .asgi_data_types.app import ASGIApp
from .request_handlers import HttpHandler, WebSocketHandler
from .routing import Router, HandlerNotFound, MatchedHandler
from storm.loggers import events_logger
from .responses import BaseHttpResponse
from .responses.http_errors import HttpError
ConfigType = TypeVar("ConfigType", bound=Mapping)


class StormApp(ASGIApp, Generic[ConfigType]):
    def __init__(
        self,
        router: Router,
        routing_executor: Executor = ThreadPoolExecutor(
            thread_name_prefix="routing_"
        ),
        debug: bool = __debug__,
        name: str = "Storm App",
        host: str = "localhost",
        config: Optional[ConfigType] = None
    ):
        self.debug = debug
        self.name = name
        self.host = host
        self.config: ConfigType = config
        self.router = router
        self.routing_executor: Executor = routing_executor

        self.router.order_routes()
        if self.config is None:
            self.config = {}

    async def http_asgi_app(
        self,
        scope: HttpASGIConnectionScope,
        receive: receive_typehint,
        send: send_typehint
    ) -> None:
        try:
            matched_handler: MatchedHandler[
                Type[HttpHandler]
            ] = await asyncio.get_running_loop(
                ).run_in_executor(
                    self.routing_executor,
                    self.router.find_http_handler,
                    scope
                )

        except HandlerNotFound:
            # TODO: return not found default response
            return

        handler: Type[HttpHandler] = matched_handler.handler
        handler_instance: HttpHandler = handler(
            self, scope, receive, matched_handler.arguments
        )

        response: BaseHttpResponse = await self.execute_handler(
            handler_instance
        )

        try:
            await self.send_http_response(send, response)

        except Exception as err:
            events_logger.error(
                "Error occurred during sending response in "
                f"http handler {handler}",
                exc_info=err
            )

        try:
            await handler_instance.on_finish()

        except Exception as err:
            events_logger.error(
                f"Error occurred during finishing http handler {handler}",
                exc_info=err
            )
            if self.debug:
                raise

    async def websocket_asgi_app(
        self,
        scope: WebSocketASGIConnectionScope,
        receive: receive_typehint,
        send: send_typehint
    ) -> None:
        try:
            matched_handler: MatchedHandler[
                Type[WebSocketHandler]
            ] = await asyncio.get_running_loop(
            ).run_in_executor(
                self.routing_executor,
                self.router.find_ws_handler,
                scope
            )

        except HandlerNotFound:
            # TODO: return not found default response
            return

        handler: Type[WebSocketHandler] = matched_handler.handler
        handler_instance: WebSocketHandler = handler(
            self, scope, receive, matched_handler.arguments
        )
        await handler_instance.execute()

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

    @staticmethod
    async def execute_handler(
        handler_instance: HttpHandler
    ) -> BaseHttpResponse:
        handler = type(handler_instance)
        response: Optional[BaseHttpResponse] = None  # noqa: there might be
        # a case when it can be not initialized

        try:
            response: Optional[BaseHttpResponse] = (
                await handler_instance.execute()
            )

        # Handle expected http errors that are also are exceptions
        except HttpError as http_error:
            response: BaseHttpResponse = http_error

        # Handle unexpected errors
        except Exception as err:
            response: Optional[BaseHttpResponse] = (
                await handler_instance.on_unexpected_error(err)
            )

            if response is None:
                events_logger.error(
                    "Unexpected errors handler didn't returned any response."
                )

        if response is None:
            events_logger.error(
                f"No response returned from http handler {handler}"
            )
            raise ValueError(
                "Any response from handler is required."
                f" (occurred in handler {handler})"
            )

        return response

    @staticmethod
    async def send_http_response(
        send: send_typehint,
        response: BaseHttpResponse
    ) -> None:
        await send(response.response_start().to_dict())
        response_body = await response.get_body()

        while True:
            response_body_event = events.HttpResponseBody(
                response_body.body,
                more_body=response_body.more_body
            )
            await send(response_body_event.to_dict())

            if not response_body_event.more_body:
                break
