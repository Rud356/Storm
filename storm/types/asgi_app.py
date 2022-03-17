"""
Module that has a base for ASGI apps like it should be for
ASGI protocol specs.
"""
from abc import ABC
from typing import Callable, Awaitable

from .asgi_supported_types import ASGI_SUPPORTED_TYPES


class ASGIApp(ABC):
    """
    Base class for ASGI apps.
    """
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
        """
        ASGI apps method that executes everything. Works only with ASGI
        spec of version 3.0.

        :param scope: connection properties.
        :param receive: method that fetches data from ASGI server.
        :param send: method to send response.
        :return: nothing.
        """
        assert scope["asgi"]["version"] == "3.0", (
            f'Only ASGI v3.0 supported, got ({scope["version"]})'
        )
