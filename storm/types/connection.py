from typing import Optional

from pydantic import BaseModel, PositiveInt


class Connection(BaseModel):
    host: str
    port: Optional[PositiveInt]
