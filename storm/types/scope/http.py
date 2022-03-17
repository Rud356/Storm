from pydantic import validator

from .base_scope import ASGIConnectionScope


class HTTPScope(ASGIConnectionScope):
    """
    Scope for some http connection.
    """
    method: str

    @classmethod
    @validator("method", pre=True)
    def parse_method(cls, value: str) -> str:
        return value.upper()

    @classmethod
    @validator("scheme")
    def validate_scheme(cls, value: str) -> str:
        if value not in {"http", "https"}:
            raise ValueError(
                "Scheme for this scope must be http or https, got "
                f" {value}"
            )
        return value
