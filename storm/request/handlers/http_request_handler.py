import re
from functools import lru_cache
from typing import TYPE_CHECKING

from storm.internal_types.asgi import HttpASGIConnectionScope, receive_typehint
from storm.responses import BaseHttpResponse
from .base_request_handler import StormBaseHandler
from ...responses.http import http_errors

if TYPE_CHECKING:
    from storm.app import StormApp


class HttpHandler(StormBaseHandler):
    scope: HttpASGIConnectionScope
    supported_methods = {
        "GET", "POST", "DELETE",
        "PATCH", "PUT", "OPTIONS"
    }

    def __init__(
        self,
        app: StormApp,
        scope: HttpASGIConnectionScope,
        receive: receive_typehint,
        parsed_arguments: re.Match
    ):
        super().__init__(app, scope, receive, parsed_arguments)

    @staticmethod
    @lru_cache(maxsize=256)
    def http_method_to_python_method(http_method_name: str) -> str:
        return http_method_name.lower()

    @property
    def default_not_implemented_response(self) -> BaseHttpResponse:
        """
        This can be used to redefine the default response
        if there's no method implemented for that http method.
        :return:
        """
        return http_errors.NotImplementedHTTP()

    async def execute(self) -> BaseHttpResponse:
        await super().execute()
        python_method_name: str = self.http_method_to_python_method(
            self.scope.method
        )
        method = getattr(self, python_method_name, None)

        if method is None:
            return self.default_not_implemented_response

        # TODO: handle method isn't implemented
        try:
            return await method()

        except NotImplementedError:
            return self.default_not_implemented_response

        except http_errors.HttpError as http_err:
            return http_err

        except Exception as unhandled_error:
            return await self.on_unexpected_error(unhandled_error)

    async def get(self) -> BaseHttpResponse:
        raise NotImplementedError()

    async def post(self) -> BaseHttpResponse:
        raise NotImplementedError()

    async def delete(self) -> BaseHttpResponse:
        raise NotImplementedError()

    async def patch(self) -> BaseHttpResponse:
        raise NotImplementedError()

    async def put(self) -> BaseHttpResponse:
        raise NotImplementedError()

    async def options(self) -> BaseHttpResponse:
        raise NotImplementedError()

    async def on_unexpected_error(
        self, exception: Exception
    ) -> BaseHttpResponse:
        self.logger.error(
            f"Unhandled exception in http handler {self}",
            exc_info=exception
        )
        return http_errors.InternalServerError()
