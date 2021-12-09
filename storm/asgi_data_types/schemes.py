from enum import Enum


class HttpScheme(Enum):
    http = "http"
    https = "https"


class WebSocketScheme(Enum):
    ws = "ws"
    wss = "wss"
