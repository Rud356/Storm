from typing import Optional

from pydantic import Field, validator

from .base_scope import ASGIConnectionScope


class WebSocketScope(ASGIConnectionScope):
    """
    Scope for websocket connection.
    """
    subprotocols: Optional[list[str]] = Field(default_factory=list)

    @classmethod
    @validator("scheme")
    def validate_scheme(cls, v: str) -> str:
        if v not in {"ws", "wss"}:
            raise ValueError(
                "Scheme for this scope must be ws or wss, got "
                f" {v}"
            )
        return v
