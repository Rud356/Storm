from abc import ABC, abstractmethod
from typing import Type

from storm.internal_types.asgi import ASGIConnectionScope
from storm.request.handlers import StormBaseHandler


class BaseRouter(ABC):
    """
    Base class for any router in app.
    """

    @abstractmethod
    def bind_handler(self, handler: Type[StormBaseHandler]):
        """
        Connects given handler to exact router.
        :param handler:
        :type handler:
        :return:
        :rtype:
        """
        pass

    @abstractmethod
    async def find_handler(
        self, scope: ASGIConnectionScope
    ) -> Type[StormBaseHandler]:
        pass
