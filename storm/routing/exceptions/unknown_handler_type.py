from .routing_exception import RoutingException


class UnknownHandlerType(RoutingException):
    """
    Raised when router got some unknown handlers type it can't process.
    """
