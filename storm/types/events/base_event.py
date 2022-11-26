from abc import ABC

from pydantic import BaseModel


class Event(BaseModel, ABC):
    """
    Any event in ASGI is having this structure.
    """
    type: str

    class Config:
        frozen: bool = True
