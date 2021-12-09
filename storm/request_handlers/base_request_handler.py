from __future__ import annotations

from abc import ABC
from functools import cached_property
from http import cookies
from typing import (
    Any, Optional, Type,
    get_args, get_type_hints, get_origin
)
from urllib.parse import parse_qs

from storm.asgi_data_types import ConnectionProperties
from storm.asgi_data_types import receive_typehint, ASGIApp
from storm.asgi_data_types.scope import ASGIConnectionScope
from storm.headers import Headers
from storm.request_parameters import BaseRequestParameter, QueryParameter
from storm.responses import BaseHttpResponse
from storm.responses.http_errors import HttpError
from .utils import parse_parameter_typehint, ParameterProperties


class StormBaseHandler(ABC):
    _query_parameters: dict[str, ParameterProperties]
    _headers_parameters: dict[str, ParameterProperties]
    _cookies_parameters: dict[str, ParameterProperties]

    def __init__(
        self,
        app: ASGIApp,  # TODO: change to base storm app
        scope: ASGIConnectionScope,
        receive: receive_typehint,
        **kwargs: Any  # noqa: may be used by other implementations
    ):
        self.app = app
        self.scope: ASGIConnectionScope = scope
        self.request_origin_path: str = scope.path
        self.headers: Headers = Headers({
            header.decode("utf-8").lower(): value.decode("utf-8")
            for header, value in scope.headers
        })
        self.cookies = cookies.SimpleCookie()
        self.cookies.load(
            self.headers.get("Cookie", "")
        )
        self.query_parameters: dict[str, str] = {
            key: value for key, value in
            parse_qs(scope.query_string).items()
        }

        self._receive: receive_typehint = receive

    async def execute(self) -> BaseHttpResponse:
        self._init_query_parameters()

        try:
            await self.prepare()

        except HttpError as http_response:
            return http_response

        except Exception as err:
            await self.on_unexpected_error(err)
            # TODO: raise internal server error

        # TODO: Select processing method

        try:
            await self.on_finish()

        except Exception as err:
            await self.on_unexpected_error(err)

    @cached_property
    def client(self) -> ConnectionProperties:
        """
        Return connection information about connected client.
        :return: ConnectionProperties instance.
        """
        return ConnectionProperties(*self.scope.client)

    @cached_property
    def server(self) -> ConnectionProperties:
        """
        Return connection information about server, to which request was made.
        :return: ConnectionProperties instance.
        """
        return ConnectionProperties(*self.scope.server)

    async def prepare(self) -> None:
        """
        This method will be called to initialize custom things,
        such as start sessions, make log entry about beginning of
        request processing, and etc. All injectables will be initialized
        by this point, all headers, cookies and query parameters will become
        attributes of class according to typehints. Also this method can be
        used to reject some requests right away by raising any class inherited
        from HttpError.

        :return: nothing.
        """
        pass

    async def on_unexpected_error(self, exception: Exception) -> None:
        pass

    async def on_finish(self) -> None:
        """
        This method is called whenever request finished processing and
        it doesn't matter if unexpected error happened, or
        everything is fine and we just finished processing.
        :return: nothing.
        """
        pass

    async def get_users_locale(self) -> Optional[str]:  # noqa:
        # used as reference method
        """
        This method can be customized to detect users locale or
        fetch it from some other place.
        :return: locale name string.
        """
        # TODO: finish this method
        return None

    def get_browsers_locale(self, default: str = "en_US") -> str:
        """
        This method is used to fetch locale from requests headers.
        :param default: default locale if none are found.
        :return: string with locale name.
        """
        # TODO: finish this method
        ...

    def __init_subclass__(cls, **kwargs) -> None:
        cls._query_parameters = {}

        for attr_key, attr_value in get_type_hints(cls).items():
            origin: Optional[Any] = get_origin(attr_value)

            if isinstance(origin, BaseRequestParameter):
                cls.__initialize_request_parameter(
                    cls, origin, attr_key, attr_value
                )

    def _init_query_parameters(self) -> None:
        for attr_key, attr_properties in self._query_parameters:
            pass

    @staticmethod
    def __initialize_request_parameter(
        cls: Type[StormBaseHandler],
        origin: BaseRequestParameter,
        attr_key: str,
        attr_value: Any
    ) -> None:
        """
        Method that prepares certain attribute to become part of class,
        when handler will be initialized.

        :param cls: class that we are currently preparing.
        :param origin: typehint that we got as origin.
        :param attr_key: attribute name in class.
        :param attr_value: attributes value, from which we are getting other
            information.
        :return: nothing.
        :raises TypeError: when typehint is not one of those: QueryParameter.
            Also may be because of invalid typehint.
        """
        # TODO: tell about how to properly typehint with subclasses of
        # BaseRequestParameter

        # Fetching all request parameters that can be set
        # right after instance was created.
        parameter_typehint: tuple[Any, ...] = get_args(
            attr_value
        )
        parameter_properties: ParameterProperties = \
            parse_parameter_typehint(
                parameter_typehint
            )

        parameter_properties.default_value = getattr(
            cls, attr_key, None
        )

        if isinstance(origin, QueryParameter):
            cls._query_parameters[attr_key] = parameter_properties

        else:
            raise TypeError(
                f"Unknown {attr_key} typehint that's "
                f"inherited from BaseRequestParameter, but "
                f"not a QueryParameter."
            )
