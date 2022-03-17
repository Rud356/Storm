from enum import Enum


from enum import Enum


class SameSite(Enum):
    """
    Used to store possible values of samesite cookie
    parameter.
    See https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie/SameSite
    for more information.
    """
    none = "None"
    strict = "Strict"
    lax = "Lax"
