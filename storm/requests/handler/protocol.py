from __future__ import annotations

from typing import (
    Any, Protocol, runtime_checkable,
    TYPE_CHECKING,
)

from storm.types import Headers, CustomCookie

if TYPE_CHECKING:
    from storm import StormApp
    from storm.types.scope.base_scope import ASGIConnectionScope


@runtime_checkable
class HandlerProtocol(Protocol):
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
        pass

    async def on_finish(self) -> None:
        """
        Clean up after finished handling request.

        :return: nothing.
        """
        pass

    async def on_unexpected_error(self, exception: Exception) -> Any:
        """
        Method that is called when caught uncaught exception, so you can
        log error and give some response at least.

        :return: some response.
        """
        pass
