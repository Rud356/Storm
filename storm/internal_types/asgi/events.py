from abc import ABC, abstractmethod

from .base_event import Event
from .supported_types import ASGI_SUPPORTED_TYPES


class HttpEvent(Event, ABC):
    """
    Base class for http related events.
    """


class HttpSendEvent(HttpEvent, ABC):
    """
    Event for sending data via http protocol.
    """

    @abstractmethod
    def to_dict(self) -> ASGI_SUPPORTED_TYPES:
        """
        Method that turns this event into something that
        ASGI server can accept.

        :return: any needed data in acceptable for ASGI server format.
        """
        raise NotImplementedError()


class HttpReceiveEvent(HttpEvent):
    """
    Event for sending data via http protocol.
    """


class HttpResponseStart(HttpSendEvent):
    """
    Event that is used to start sending a response.
    """
    type: str = "http.request"

    def __init__(self, status: int, headers: list[tuple[bytes, bytes]]):
        self.status: int = status
        self.headers: list[tuple[bytes, bytes]] = headers

    def to_dict(self) -> ASGI_SUPPORTED_TYPES:
        return {
            "type": self.type,
            "status": self.status,
            "headers": self.headers
        }


class HttpResponseBody(HttpSendEvent):
    """
    Event that is used for sending responses body.
    """
    type: str = "http.request.body"

    def __init__(self, body: bytes = b"", more_body: bool = False):
        self.body: bytes = body
        self.more_body: bool = more_body

    def to_dict(self) -> ASGI_SUPPORTED_TYPES:
        return {
            "type": self.type,
            "body": self.body,
            "more_body": self.more_body
        }


class HttpRequest(HttpReceiveEvent):
    """
    Event sent to Storm when got new request.
    """
    type: str = "http.request"

    def __init__(self, body: bytes = b"", more_body: bool = False):
        self.body: bytes = body
        self.more_body: bool = more_body


class HttpDisconnect(HttpReceiveEvent):
    """
    Event send to Storm when connection is closed.
    """
    type: str = "http.disconnect"

    def __init__(self):
        # We don't need to do anything here
        pass
