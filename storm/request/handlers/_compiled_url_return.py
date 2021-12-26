from re import Pattern
from typing import NamedTuple


class CompiledUrl(NamedTuple):
    url_pattern: Pattern
    is_static_url: bool
