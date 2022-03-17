from __future__ import annotations

from abc import ABC
from typing import Any, TYPE_CHECKING

from storm.types import Headers, CustomCookie

if TYPE_CHECKING:
    from storm import StormApp
    from storm.types.scope.base_scope import ASGIConnectionScope


class HandlerProtocol(ABC):
    app: StormApp
    scope: ASGIConnectionScope
    request_origin_url: str
    headers: Headers
    cookies: CustomCookie

    async def prepare(self) -> None:
        """
        Function that initializes things before starting handling.

        :return: nothing.
        """

    async def execute(self) -> Any:
        """
        Method that runs handling of request.

        :return: some response.
        """

    async def on_finish(self) -> None:
        """
        Clean up after finished handling request.

        :return: nothing.
        """

    async def on_unexpected_error(self, exception: Exception) -> Any:
        """
        Method that is called when caught uncaught exception, so you can
        log error and give some response at least.

        :return: some response.
        """
