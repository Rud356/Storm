from .routing_exception import RoutingException


class HandlerNotFound(RoutingException):
    """
    Raised when this router doesn't have any handlers that matches.
    """