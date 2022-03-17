from storm.types.events.base_event import Event


class Startup(Event):
    """
    Server starts up.
    """
    type: str = "lifespan.startup"


class Shutdown(Event):
    """
    Server is shutting down.
    """
    type: str = "lifespan.shutdown"
