from typing import TypeVar

from storm.requests.parameters.protocol import Parameter

UrlParam = TypeVar("UrlParam")


class URLParameter(Parameter[UrlParam]):
    """
    Class that represents url parameters, that will be used to compile urls.
    """
    def __init__(self, parameter: UrlParam):
        super().__init__(parameter)

