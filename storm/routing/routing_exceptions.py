class NotMatchingRule(KeyError):
    """
    Raised if passed scope not matches the rule.
    """


class HandlerNotFound(KeyError):
    """
    Raised if no handler for passed scope is found.
    """


class NotUniqueHandlerUrl(ValueError):
    """
    Raised when there are two handlers bound to the router.
    """
