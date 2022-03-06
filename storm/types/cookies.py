from http.cookies import SimpleCookie


class CustomCookie(SimpleCookie):
    """
    Class for storing cookies and outputting them in
    form that works with ASGI server.
    """
    def as_headers_list(
        self,
        header: bytes = b"set-cookie"
    ) -> list[list[bytes]]:
        result = []
        items = sorted(self.items())

        for _, value in items:
            # Encode values of cookies and pass known header name
            result.append(
                [
                    header,
                    value.OutputString().encode('utf-8')
                ]
            )

        return result
