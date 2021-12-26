from __future__ import annotations

import re
from abc import ABC, abstractmethod
from functools import cached_property
from typing import (
    Any, Optional, Type,
    get_args, get_type_hints, get_origin,
    TYPE_CHECKING, Mapping
)
from urllib.parse import parse_qs

from storm.headers import Headers
from storm.internal_types import LocaleProbability, CustomCookie
from storm.internal_types.asgi import ASGIConnectionScope
from storm.internal_types.asgi import ConnectionProperties
from storm.internal_types.asgi import receive_typehint
from storm.loggers import handler_logger
from storm.request.parameters import (
    BaseRequestParameter,
    QueryParameter,
    CookieParameter,
    URLParameter
)
from storm.request.parameters.url import compile_type_to_named_group
from .utils import parse_parameter_typehint, ParameterProperties
from ._compiled_url_return import CompiledUrl

if TYPE_CHECKING:
    from storm.app import StormApp


class StormBaseHandler(ABC):
    url: str
    is_static_url: bool = True

    _query_parameters_properties: dict[str, ParameterProperties]
    _url_parameters_properties: dict[str, ParameterProperties]
    _cookies_properties: dict[str, ParameterProperties]

    def __init__(
        self,
        app: StormApp,
        scope: ASGIConnectionScope,
        receive: receive_typehint,
        parsed_arguments: re.Match
    ):
        self.app = app
        self.scope: ASGIConnectionScope = scope
        self.url: str = scope.path
        self.request_origin_path: str = scope.path
        self.headers: Headers = Headers()
        for header, values_str in scope.headers:
            self.headers[header.decode('utf-8')] = values_str.decode('utf-8')

        self.cookies: CustomCookie = CustomCookie()
        self.cookies.load(
            self.headers.get("Cookie", "")
        )
        self.query_parameters: dict[str, list[str]] = {}

        if scope.query_string is not None:
            for key, values in parse_qs(
                scope.query_string.decode("utf-8")
            ).items():
                assert (
                    isinstance(key, str) and
                    all([isinstance(value, str)for value in values])
                ), (
                    "After string was decoded parse_qs must only "
                    "return strings."
                )

                self.query_parameters[
                    key
                ] = [v for v in values]

        self.logger = handler_logger
        self._receive: receive_typehint = receive
        self._parsed_arguments: re.Match = parsed_arguments

    @abstractmethod
    async def execute(self) -> Any:
        self._init_query_parameters()
        self._init_cookie_parameters()
        self._init_url_parameters()
        # TODO: add init of injectables
        await self.prepare()

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
        used to reject some requests right away.

        :return: nothing.
        """
        pass

    async def on_unexpected_error(self, exception: Exception) -> Any:
        """
        Gives some response when unexpected error occurred.
        :param exception: some unhandled exception.
        :return: any suiting response instance.
        """
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
        return None

    def get_browsers_locales(self, default: str = "en_US") -> list[LocaleProbability]:
        """
        This method is used to fetch locales from requests headers.
        :param default: default locale if none are found.
        :return: list of named tuples, sorted by weight.
        """
        # Based on tornado implementation:
        # https://github.com/tornadoweb/tornado/blob/208672f3bf6cbb7e37f54c356e02a71ca29f1e02/tornado/web.py#L1279
        if 'Accept-Language' not in self.headers:
            return [LocaleProbability(default, 1.0)]

        try:
            languages = self.headers['Accept-Language'][0].split(',')

        except IndexError:
            return [LocaleProbability(default, 1.0)]

        locales = []

        for language in languages:
            parts = language.strip().partition(";")
            score = 0.0
            if parts[1].startswith('q='):
                try:
                    score = float(parts[1][:2])

                except (ValueError, TypeError):
                    pass

            else:
                score = 1.0

            locales.append(LocaleProbability(parts[0], score))

        if locales:
            locales.sort(key=lambda v: v.weight)
            return locales

        return [LocaleProbability(default, 1.0)]

    @property
    def config(self) -> Mapping:
        return self.app.config

    def __init_subclass__(cls, **kwargs) -> None:
        cls.is_static_url = True
        cls._query_parameters_properties = {}
        cls._url_parameters_properties = {}
        cls._cookies_properties = {}

        for attr_key, attr_value in get_type_hints(cls).items():
            origin: Optional[Any] = get_origin(attr_value)

            if isinstance(origin, BaseRequestParameter):
                cls.__initialize_request_parameter(
                    cls, origin, attr_key, attr_value
                )

    def _init_query_parameters(self) -> None:
        """
        Initializes query parameters as attributes of handler.
        :returns: nothing.
        """
        for attr_key, attr_properties in self. \
                _query_parameters_properties.items():

            if attr_properties.is_optional:
                attr_value: Any = self.query_parameters.get(
                    attr_key,
                    attr_properties.default_value
                )

            else:
                attr_value = self.query_parameters[attr_key]

            attr_value = attr_properties.casted_to_type(attr_value)
            setattr(self, attr_key, attr_value)

    def _init_cookie_parameters(self) -> None:
        """
        Initializes received cookies as attributes of handler. Before
        being assigned they are casted
        :returns: nothing.
        """
        for attr_key, attr_properties in self. \
                _cookies_properties.items():

            try:
                attr_value: Any = self.cookies[attr_key].value

            except KeyError:
                if attr_properties.is_optional:
                    attr_value = attr_properties.default_value

                else:
                    raise

            casted_value: type = attr_properties.casted_to_type(attr_value)
            setattr(self, attr_key, casted_value)

    def _init_url_parameters(self) -> None:
        """
        Initializes query parameters as attributes of handler.
        :returns: nothing.
        """
        for attr_key, attr_properties in self. \
                _url_parameters_properties.items():
            try:
                attr_value: Any = self._parsed_arguments.group(
                    attr_key
                )
                attr_value = attr_properties.casted_to_type(attr_value)
                setattr(self, attr_key, attr_value)

            except IndexError as err:
                raise KeyError(
                    f"Group with name {attr_key} not found"
                    f" in url parameters, but url was matched."
                    f"(\n\tfound_parameters: {self._parsed_arguments}\n"
                ) from err

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

        if parameter_properties.is_optional:
            parameter_properties.default_value = getattr(
                cls, attr_key, None
            )

        if isinstance(origin, QueryParameter):
            cls._query_parameters_properties[attr_key] = parameter_properties

        elif isinstance(origin, CookieParameter):
            cls._cookies_properties[attr_key] = parameter_properties

        elif isinstance(origin, URLParameter):
            if parameter_properties.is_optional:
                raise ValueError("URL parameters can not be optional")

            cls.is_static_url = False
            cls._url_parameters_properties[attr_key] = parameter_properties

    @staticmethod
    def _compile_url_regex(
        cls: Type[StormBaseHandler],
        url: str
    ) -> CompiledUrl:
        """
        Compiles url into url_regex that will be used when looking
        for a route based on found URLParameter type hints.

        :param cls: subclass of StormBaseHandler we are initializing.
        :return: re.compile output after manipulations and is url static.
        """
        parameters_names_regex = re.compile(r"<(\w+)>")
        parameters_names: set[str] = set(
            parameters_names_regex.findall(
                url
            )
        )

        # Validating all names in url
        invalid_names = []
        for parameter_name in parameters_names:
            if not parameter_name.isidentifier():
                invalid_names.append(parameter_name)

        if invalid_names:
            raise KeyError(
                f"Following url parameters are invalid "
                f"in handler {cls.__name__}: {invalid_names}. "
                f"All parameters names must be a valid python identifiers."
            )

        # We have to make sure all url parameters are used in url
        url_params_difference = set(
            cls._url_parameters_properties.keys()
        ).difference(parameters_names)

        if url_params_difference:
            raise KeyError(
                "Following url parameters aren't "
                "represented in handlers url "
                f"({url}):\n{url_params_difference}"
            )

        compiled_url = url
        for parameter in parameters_names:
            url_parameters_properties: Optional[ParameterProperties] = \
                cls._url_parameters_properties.get(
                    parameter
                )

            if url_parameters_properties is None:
                continue

            compiled_url = re.sub(
                r"<%s>" % parameter, compiled_url,
                compile_type_to_named_group(
                    parameter,
                    url_parameters_properties.casted_to_type
                )
            )

        has_url_parameters = bool(cls._url_parameters_properties)
        compiled_url_regex = re.compile(compiled_url)
        return CompiledUrl(
            url_pattern=compiled_url_regex,
            is_static_url=has_url_parameters
        )

    def __str__(self):
        return f"{self.__name__} on url {self.url}"
