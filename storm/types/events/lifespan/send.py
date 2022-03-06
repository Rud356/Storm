from typing import Optional

from storm.types.events.base_event import Event


class StartupComplete(Event):
    """
    Server finished startup.
    """
    type: str = "lifespan.startup.complete"


class StartupFailed(Event):
    """
    Framework failed to start due to some issue.
    """
    type: str = "lifespan.startup.failed"
    message: Optional[str] = ""


class ShutdownComplete(Event):
    """
    Framework been successfully shut down.
    """
    type: str = "lifespan.shutdown.complete"


class ShutdownFailed(Event):
    """
    Framework failed to shut down.
    """
    type: str = "lifespan.shutdown.failed"
    message: str = ""
