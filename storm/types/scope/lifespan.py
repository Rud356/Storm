from pydantic import Field

from storm.types.scope.base_scope import BaseScope


class LifespanScope(BaseScope):
    """
    Scope used for lifespan events
    """
    type: str = Field(const=True, default="lifespan")
