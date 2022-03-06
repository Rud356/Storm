from typing import Optional, Iterable, Any

from pydantic import BaseModel, Field, validator

from storm.types.connection import Connection
from storm.types.headers import Headers


class ASGIData(BaseModel):
    version: str
    spec_version: Optional[str] = Field(default="2.0")

    class Config:
        frozen: bool = True


class BaseScope(BaseModel):
    type: str
    asgi: ASGIData
    extensions: Optional[dict[str, str]] = Field(default_factory=dict)


class ASGIConnectionScope(BaseScope):
    """
    Scope that is used when some connection is initiated.
    """
    http_version: str
    scheme: str
    path: str
    root_path: str
    raw_path: Optional[str]
    query_string: Optional[str]
    headers: Headers
    client: Connection
    server: Connection

    @classmethod
    @validator("client", pre=True)
    def parse_client(cls, v: Any) -> Connection:
        return cls.parse_connection(v)

    @classmethod
    @validator("server", pre=True)
    def parse_server(cls, v: Any) -> Connection:
        return cls.parse_connection(v)

    @classmethod
    def parse_connection(
        cls,
        value: tuple[str, Optional[int]]
    ) -> Connection:
        """
        Parse connection properties from received list.

        :param value: anything.
        :return: Connection instance.
        """
        if not isinstance(value, list):
            raise ValueError(
                "ASGI server must give list, which contain two values: "
                "host and port"
            )

        if len(list) != 2:
            raise ValueError(
                "Host and port must be supplied by server, "
                "and even if connected through unix socket - supply None "
                "instead of port"
            )

        return Connection(host=value[0], port=value[1])

    @classmethod
    @validator("headers", pre=True)
    def parse_headers(cls, v: Any) -> Headers:
        if not isinstance(v, list):
            raise ValueError("Headers must be a list")

        return Headers.from_list(v)