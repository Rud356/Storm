from typing import Optional

from storm.loggers import events_logger
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

    @classmethod
    def emit_startup_finished(cls) -> dict:
        return {
            "type": cls.type
        }


class StartupFailed(LifetimeEvent):
    """
    Framework failed to start due to some issue.
    """
    type: str = "lifespan.startup.failed"

    def __init__(self, message: Optional[str] = None):
        self.message: str = message or ""

    def emit_startup_failed(self):
        return {
            "type": self.type,
            "message": self.message
        }


class Shutdown(LifetimeEvent):
    """
    Server is shutting down.
    """
    type: str = "lifespan.shutdown"


class ShutdownComplete(LifetimeEvent):
    """
    Framework been successfully shut down.
    """
    type: str = "lifespan.shutdown.complete"

    @classmethod
    def emit_shutdown_complete(cls) -> str:
        """
        Gives text that needs to be sent to ASGI server to complete shutdown.

        :return: string that will shut down ASGI server.
        """
        return cls.type


class ShutdownFailed(LifetimeEvent):
    """
    Framework failed to shut down.
    """
    type: str = "lifespan.shutdown.failed"

    def __init__(self, message: Optional[str] = None):
        self.message = message or ""

    def emit_server_shutdown_failure(
        self
    ) -> dict[str, str]:
        """
        Gives dict that will tell server that shutdown
        failed and optionally a reason why.

        :return: dictionary with message.
        """

        events_logger.error(f"Shutdown failed with message: {self.message}")
        return {
            "type": self.type,
            "message": self.message
        }


def dispatch_incoming_lifetime_event(event_type: str) -> Event:
    known_events = {
        Startup.type: Startup,
        Shutdown.type: Shutdown
    }
    return known_events[event_type]()
