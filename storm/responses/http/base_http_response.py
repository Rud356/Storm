from abc import ABC, abstractmethod
from datetime import timedelta
from typing import Union, Optional

from storm.headers import Headers
from storm.internal_types import CustomCookie
from .cookie_same_site_parameter import SameSite
from .response_body import ResponseBody
from ...internal_types.asgi import events


class BaseHttpResponse(ABC):
    status: int
    headers: Headers
    cookies: CustomCookie

    def response_start(self) -> events.HttpResponseStart:
        headers: list[tuple[bytes, bytes]] = self.headers.to_list()
        headers.extend(self.cookies.as_headers_list())

        return events.HttpResponseStart(
            self.status,
            headers
        )

    @abstractmethod
    async def get_body(self) -> ResponseBody:
        """
        Method that will give us parts of body that we have to send.
        Set flag more_body, if method needs to be called once again and
        we have more bytes to send.
        :return: ResponseBody instance. By default is empty.
        """
        return ResponseBody()

    def set_cookie(
        self,
        name: str,
        value: str,
        max_age: Union[int, float, timedelta],
        path: str = "/",
        domain: Optional[str] = None,
        httponly: bool = False,
        secure: bool = False,
        same_site: Union[str, SameSite] = SameSite.strict
    ) -> None:
        """
        Sets a cookie for this response.

        :param name: cookie name.
        :param value: cookies value.
        :param max_age: how long this cookie will live in browser.
        :param path: on what path it works.
        :param domain: on what domain this cookie will be working.
        :param httponly: sets if cookie isn't available for js in browser.
        :param secure: sets if cookie can only be sent when securely connected.
        :param same_site: sets permissions on what sites can send this cookie.
            By default in strict mode.
        :return: nothing.
        :raises TypeError: if passed not int or float to max_age argument.
        :raises KeyError: if passed invalid same_site
            (not from keys of SameSite, or SameSite attribute).
        """
        self.cookies[name] = value
        self.cookies[name]["path"] = path
        self.cookies[name]["domain"] = domain
        self.cookies[name]["httponly"] = httponly
        self.cookies[name]["secure"] = secure

        if isinstance(same_site, SameSite):
            # We must ignore mypy here because it refuses to understand
            # that enum must have this value as string
            self.cookies[name]["samesite"] = same_site.strict.value   # type: ignore

        elif isinstance(same_site, str):
            self.cookies[name]["samesite"] = SameSite[same_site].value

        else:
            raise ValueError(
                f"Unknown type for same_site parameter: {type(same_site)}"
            )

        if isinstance(max_age, float):
            self.cookies[name]["max-age"] = max_age

        elif isinstance(max_age, timedelta):
            self.cookies[name]["max-age"] = max_age.total_seconds()

        else:
            raise TypeError(
                "Invalid type for max_age argument. "
                f"Expected float or timedelta (got {type(max_age)})"
            )

    def delete_cookie(
        self, name: str, path: str = "/", domain: Optional[str] = None
    ) -> None:
        """
        Deletes some cookie on client side.

        :param name: cookie name.
        :param path: on what path it works.
        :param domain: on what domain this cookie will be working.
        :returns: nothing.
        """
        self.set_cookie(
            name=name, value="", max_age=0,
            path=path, domain=domain
        )

    def delete_cookies(
        self, *names: str, path: str = "/", domain: Optional[str] = None
    ):
        """
        Deletes some cookie on client side.

        :param names: cookies names that will be cleared.
        :param path: on what path it works.
        :param domain: on what domain this cookie will be working.
        :returns: nothing.
        """
        for name in names:
            self.delete_cookie(name, path, domain)
