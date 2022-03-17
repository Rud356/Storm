from .routing_exception import RoutingException


class NotMatchingRule(RoutingException):
    """
    Raised when supplied scope doesn't match the rule.
    """
    pass
