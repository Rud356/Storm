from abc import ABC
from dataclasses import dataclass, field
from typing import Iterable, Optional


class BaseASGIScope(ABC):
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


class ASGIConnectionScope(BaseASGIScope):
    """
    Base class for any connection from ASGI server.
    """
    def __init__(
        self,
        *,
        type: str,
        asgi: dict[str, str],
        extensions: dict[str, dict],
        http_version: str,
        scheme: str,
        path: str,
        root_path: str,
        raw_path: Optional[str],
        query_string: Optional[bytes],
        headers: Iterable[tuple[bytes, bytes]],
        client: Iterable[tuple[str, Optional[int]]],
        server: Iterable[tuple[str, Optional[int]]],
    ):
        self.type: str = type
        self.asgi: dict[str, str] = asgi
        self.extensions: extensions = extensions
        self.http_version: str = http_version
        self.scheme: str = scheme
        self.path: str = path
        self.root_path: str = root_path
        self.raw_path: Optional[str] = raw_path
        self.query_string: Optional[bytes] = query_string
        self.headers: Iterable[tuple[bytes, bytes]] = headers
        self.client: Iterable[tuple[str, Optional[int]]] = client
        self.server: Iterable[tuple[str, Optional[int]]] = server

        self.__post_init__()

    def __post_init__(self):
        assert self.asgi_version in {"3.0"}, (
            "Asgi version doesn't match with supported by storm"
            " (must be 3.0 only)"
        )

        assert self.asgi_spec_version in {"2.0", "2.1"}, (
            "Asgi spec_version must be only 2.1 or 2.0"
        )


class HttpASGIConnectionScope(ASGIConnectionScope):
    """
    Class for HTTP connection scope parameters.
    """
    def __init__(
        self,
        *,
        type: str,
        asgi: dict[str, str],
        extensions: dict[str, dict],
        http_version: str,
        scheme: str,
        path: str,
        root_path: str,
        raw_path: Optional[str],
        query_string: Optional[bytes],
        headers: Iterable[tuple[bytes, bytes]],
        client: Iterable[tuple[str, Optional[int]]],
        server: Iterable[tuple[str, Optional[int]]]
    ):
        super(HttpASGIConnectionScope, self).__init__(
            type=type or "http", asgi=asgi, extensions=extensions,
            http_version=http_version, scheme=scheme or "http",
            path=path, root_path=root_path, raw_path=raw_path or None,
            query_string=query_string, headers=headers,
            client=client, server=server
        )

    def __post_init__(self):
        super().__post_init__()
        assert self.scheme in {"http", "https"}, (
            f"Invalid scheme for HttpAsgiConnectionScope (got {self.scheme}"
        )


class WebSocketASGIConnectionScope(ASGIConnectionScope):
    """
    Class for WebSockets ASGI connections scope.
    """
    type: str = field(default="websocket")
    scheme: str = field(default="ws")
    raw_path: Optional[str] = field(default=None)
    subprotocols: Iterable[str] = field(default_factory=list)

    def __init__(
        self,
        *,
        type: str,
        asgi: dict[str, str],
        extensions: dict[str, dict],
        http_version: str,
        scheme: str,
        path: str,
        root_path: str,
        raw_path: Optional[str],
        query_string: Optional[bytes],
        headers: Iterable[tuple[bytes, bytes]],
        client: Iterable[tuple[str, Optional[int]]],
        server: Iterable[tuple[str, Optional[int]]],
        subprotocols: Iterable[str]
    ):
        self.subprotocols: Iterable[str] = subprotocols or []
        super(WebSocketASGIConnectionScope, self).__init__(
            type=type or "websocket", asgi=asgi, extensions=extensions,
            http_version=http_version, scheme=scheme or "ws",
            path=path, root_path=root_path, raw_path=raw_path or None,
            query_string=query_string, headers=headers,
            client=client, server=server
        )

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
