from typing import Iterable, Union, Optional
from dataclasses import dataclass, field


@dataclass(frozen=True)
class ASGIConnectionScope:
    type: str
    asgi: dict[str, str]
    http_version: str
    scheme: str
    path: str
    raw_path: Optional[str]
    query_string: str
    root_path: str
    headers: Iterable[tuple[bytes, bytes]]
    client: Iterable[
        Union[tuple[str, int], tuple[str, None]]
    ]
    server: Iterable[
        Union[tuple[str, int], tuple[str, None]]
    ]

    def __post_init__(self):
        assert self.asgi_version in {"3.0"}, (
            "Asgi version doesn't match with supported by storm"
            " (must be 3.0 only)"
        )

    @property
    def asgi_version(self) -> str:
        return self.asgi.get("version", default="2.0")

    @property
    def asgi_spec_version(self) -> str:
        return self.asgi.get("spec_version", default="2.0")


@dataclass(frozen=True)
class HttpASGIConnectionScope(ASGIConnectionScope):
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
