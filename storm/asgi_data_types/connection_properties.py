from typing import NamedTuple, Optional


class ConnectionProperties(NamedTuple):
    origin: str
    port: Optional[int]
