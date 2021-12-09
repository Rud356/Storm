from http.cookies import SimpleCookie
from typing import Any, Optional

from storm.headers import Headers
from .. import ResponseBody
from ..base_http_response import BaseHttpResponse
from ..response_encoders import BaseResponseEncoder
from ..response_encoders import TextEncoder


class HttpError(Exception, BaseHttpResponse):
    def __init__(
        self,
        status: int,
        headers: Optional[Headers] = None,
        cookies: Optional[SimpleCookie] = None,
        message: Optional[Any] = None,
        response_encoder: BaseResponseEncoder = TextEncoder()
    ):
        self.status = status
        self.headers = headers
        self.cookies = cookies
        self.message = message
        self.response_encoder = response_encoder

        if self.headers is None:
            self.headers = Headers()

        if self.cookies is None:
            self.cookies = SimpleCookie()

    async def get_body(self) -> ResponseBody:
        if self.message is not None:
            return ResponseBody(
                body=self.message.encode('utf-8')
            )

        else:
            return ResponseBody()
