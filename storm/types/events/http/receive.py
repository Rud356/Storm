from abc import ABC

from storm.types.events.base_event import Event


class HttpReceiveEvent(Event, ABC):
    """
    Event for sending data via http protocol.
    """


class HttpRequest(HttpReceiveEvent):
    """
    Event sent to Storm when got new request.
    """
    type: str = "http.request"
    body: bytes
    more_body: bool


class HttpDisconnect(HttpReceiveEvent):
    """
    Event send to Storm when connection is closed.
    """
    type: str = "http.disconnect"
