from abc import ABC, abstractmethod

from storm.types.asgi_supported_types import ASGI_SUPPORTED_TYPES
from storm.types.events.base_event import Event
from storm.types.headers import Headers


class HttpSendEvent(Event, ABC):
    """
    Used for sending data back to ASGI server as response.
    """
    @abstractmethod
    def to_dict(self) -> ASGI_SUPPORTED_TYPES:
        """
        Method that turns this event into something that
        ASGI server can accept.

        :return: any needed data in acceptable for ASGI server format.
        """
        raise NotImplementedError()


class ResponseStart(HttpSendEvent):
    type: str = "http.response.start"
    status: int
    headers: Headers

    def to_dict(self) -> ASGI_SUPPORTED_TYPES:
        return {
            "type": self.type,
            "status": self.status,
            "headers": self.headers
        }


class ResponseBody(HttpSendEvent):
    type: str = "http.request.body"
    body: bytes = b""
    more_body: bool = False

    def to_dict(self) -> ASGI_SUPPORTED_TYPES:
        return {
            "type": self.type,
            "body": self.body,
            "more_body": self.more_body
        }
