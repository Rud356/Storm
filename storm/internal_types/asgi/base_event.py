from abc import ABC


class Event(ABC):
    """
    Class that is used as base for any
    events related to ASGI app.
    """
    type: str

