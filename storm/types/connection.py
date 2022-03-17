from typing import Optional, NamedTuple

from pydantic import PositiveInt


class Connection(NamedTuple):
    host: str
    port: Optional[PositiveInt]
