from typing import Any, Optional

from storm.headers import Headers
from storm.internal_types import CustomCookie
from storm.responses.encoders import BaseResponseEncoder
from storm.responses.encoders import TextEncoder
from storm.responses.http import ResponseBody
from ..base_http_response import BaseHttpResponse


class HttpError(Exception, BaseHttpResponse):
    def __init__(
        self,
        status: int,
        headers: Optional[Headers] = None,
        cookies: Optional[CustomCookie] = None,
        message: Optional[Any] = None,
        response_encoder: BaseResponseEncoder = TextEncoder()
    ):
        self.status = status
        self.headers = headers or Headers()
        self.cookies = cookies or CustomCookie()
        self.message = message
        self.response_encoder = response_encoder

    async def get_body(self) -> ResponseBody:
        if self.message is not None:
            return ResponseBody(
                body=self.message.encode('utf-8')
            )

        else:
            return ResponseBody()
