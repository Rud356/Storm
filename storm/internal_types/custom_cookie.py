from http.cookies import SimpleCookie


class CustomCookie(SimpleCookie):
    def as_headers_list(
        self,
        header: bytes = b"set-cookie:"
    ) -> list[tuple[bytes, bytes]]:
        result = []
        items = sorted(self.items())
        for _, value in items:
            result.append(
                (
                    header,
                    value.output(header="").strip(" ").encode('utf-8')
                )
            )
        return result
