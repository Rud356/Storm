from dataclasses import dataclass, field
from typing import Iterable, Optional


@dataclass(frozen=True)
class BaseASGIScope:
    """
    Base class for any ASGI scope.
    """
    type: str
    asgi: dict[str, str]
    extensions: dict[str, dict]

    @property
    def asgi_version(self) -> str:
        return self.asgi.get("version", default="2.0")

    @property
    def asgi_spec_version(self) -> str:
        return self.asgi.get("spec_version", default="2.0")


@dataclass(frozen=True)
class ASGIConnectionScope(BaseASGIScope):
    """
    Base class for any connection from ASGI server.
    """
    http_version: str
    scheme: str
    path: str
    root_path: str
    raw_path: Optional[str]
    query_string: Optional[bytes]
    headers: Iterable[tuple[bytes, bytes]]
    client: Iterable[tuple[str, Optional[int]]]
    server: Iterable[tuple[str, Optional[int]]]

    def __post_init__(self):
        assert self.asgi_version in {"3.0"}, (
            "Asgi version doesn't match with supported by storm"
            " (must be 3.0 only)"
        )

        assert self.asgi_spec_version in {"2.0", "2.1"}, (
            "Asgi spec_version must be only 2.1 or 2.0"
        )


@dataclass(frozen=True)
class HttpASGIConnectionScope(ASGIConnectionScope):
    """
    Class for HTTP connection scope parameters.
    """
    type: str = field(default="http")
    scheme: str = field(default="http")
    raw_path: Optional[str] = field(default=None)

    def __post_init__(self):
        super().__post_init__()
        assert self.scheme in {"http", "https"}, (
            f"Invalid scheme for HttpAsgiConnectionScope (got {self.scheme}"
        )


@dataclass(frozen=True)
class WebSocketASGIConnectionScope(ASGIConnectionScope):
    """
    Class for WebSockets ASGI connections scope.
    """
    type: str = field(default="websocket")
    scheme: str = field(default="ws")
    raw_path: Optional[str] = field(default=None)
    subprotocols: Iterable[str] = field(default_factory=list)

    def __post_init__(self):
        super().__post_init__()
        assert self.scheme in {"ws", "wss"}, (
            "Invalid scheme for WebSocketAsgiConnectionScope "
            f"(got {self.scheme})"
        )


@dataclass(frozen=True)
class LifetimeASGIScope(BaseASGIScope):
    """
    Class that represents lifetime messages from ASGI server.
    """
