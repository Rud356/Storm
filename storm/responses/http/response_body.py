from typing import NamedTuple


class ResponseBody(NamedTuple):
    """
    Class that will be used to know if everything that been
    sent is everything we have to send, and to deliver what bytes should
    be sent.
    """
    body: bytes = b""
    more_body: bool = False
