from typing import Optional

from .base_event import Event


class LifetimeEvent(Event):
    """
    Event that is related to lifecycle of app.
    """


class Startup(LifetimeEvent):
    """
    Server starts up.
    """
    type: str = "lifespan.startup"


class StartupComplete(LifetimeEvent):
    """
    Server finished startup.
    """
    type: str = "lifespan.startup.complete"


class StartupFailed(LifetimeEvent):
    """
    Server failed to start due to some issue.
    """
    type: str = "lifespan.startup.failed"

    def __init__(self, message: Optional[str] = None):
        self.message: str = message or ""


class Shutdown(LifetimeEvent):
    """
    Server is shutting down.
    """
    type: str = "lifespan.shutdown"


class ShutdownComplete(LifetimeEvent):
    type: str = "lifespan.shutdown.complete"

    @classmethod
    def emit_shutdown_complete(cls) -> str:
        """
        Gives text that needs to be sent to ASGI server to complete shutdown.

        :return: string that will shut down ASGI server.
        """
        return cls.type


class ShutdownFailed(LifetimeEvent):
    type: str = "lifespan.shutdown.failed"

    @classmethod
    def emit_server_shutdown_failure(
        cls, message: Optional[str] = None
    ) -> dict[str, str]:
        """
        Gives dict that will tell server that shutdown
        failed and optionally a reason why.

        :param message: reason why shutdown failed.
        :return: dictionary with message.
        """
        message = message or None
        return {
            "type": cls.type,
            "message": message
        }
