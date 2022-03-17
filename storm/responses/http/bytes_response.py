from typing import Optional

from storm.types import Headers, CustomCookie
from .base_http_response import BaseHttpResponse
from .response_body import ResponseBody


class BytesResponse(BaseHttpResponse):
    def __init__(
        self,
        status: int,
        body: bytes,
        headers: Optional[Headers] = None,
        cookies: Optional[CustomCookie] = None
    ):
        self.status: int = status
        self.body: bytes = body
        self.headers: Headers = headers or Headers()
        self.cookies: CustomCookie = cookies or CustomCookie()

    async def get_body(self) -> ResponseBody:
        return ResponseBody(
            body=self.body,
            more_body=False
        )
