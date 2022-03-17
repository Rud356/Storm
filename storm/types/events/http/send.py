from abc import ABC

from storm.types.events.base_event import Event
from storm.types.headers import Headers


class HttpSendEvent(Event, ABC):
    """
    Used for sending data back to ASGI server as response.
    """


class ResponseStart(HttpSendEvent):
    type: str = "http.response.start"
    status: int
    headers: Headers


class ResponseBody(HttpSendEvent):
    type: str = "http.response.body"
    body: bytes = b""
    more_body: bool = False
