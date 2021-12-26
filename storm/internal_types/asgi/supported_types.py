from typing import Union

# Alas, but mypy can not understand what the hell been going on here
ASGI_SUPPORTED_TYPES = Union[
    str, bytes, int, float,
    bool, None, list, dict
]
