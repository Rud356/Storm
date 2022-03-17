from .routing_exception import RoutingException


class UnknownScopeType(RoutingException):
    """
    Raised when router got some unknown scope type it can't process.
    """
