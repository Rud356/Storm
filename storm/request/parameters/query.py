from .base_request_parameter import BaseRequestParameter


class QueryParameter(BaseRequestParameter):
    """
    Class for treating request query arguments as attributes
    with specific types. Name of type hinted argument will match query
    parameters name.

    Examples:

    .. code-block:: python

        class A(StormBaseHandler):
            q: QueryParameter[int]

            def get(self):
                print(type(self.q))  # int

    .. code-block:: python

        class A(StormBaseHandler):
            q: QueryParameter[typing.Optional[int]] = 1

            def get(self):
                # If we got no value in query arguments - we will get default
                # as value of 1.
                # If default isn't provided - there will be None.
                print(self.q)  # 1
    """
