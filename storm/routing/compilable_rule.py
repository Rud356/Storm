import re
from typing import Type

from storm.requests.handlers import HandlerProtocol
from .regex_rule import RegexRule


class CompilableRule(RegexRule):
    """
    This class instead of requiring to give it prepared regex and expect
    that all parameters will match instead builds regex from supplied string.
    To insert any parameter you should just use <variable_name> notation.
    For example: /api/<version>. Then all parameters that are listed in handlers
    using URLParam[type] will be collected from handlers and their names will be
    looked inside of <> to be replaced with regex.

    .. code-block:: python
    class Handler(HttpHandler):
        version: int

    CompilableRule("/api/<version>", Handler)
    # Here it will transform into r"/api/\\d+" regex
    """
    def __init__(self, url: str, handler: Type[HandlerProtocol]):
        super().__init__(url, handler)
        self.regex = self.compile_regex_for_handler()

    def compile_regex_for_handler(self) -> re.Pattern:
        # TODO: add way to compile regex from handlers information
        pass
