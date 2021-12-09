from .response_encoder import BaseResponseEncoder


class TextEncoder(BaseResponseEncoder):
    def __init__(self, encoding: str = "utf-8"):
        self.encoding = encoding

    def encode(self, data: str) -> bytes:
        return data.encode(encoding=self.encoding)
