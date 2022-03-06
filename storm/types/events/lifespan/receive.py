from storm.types.events import Event


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
