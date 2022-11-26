from string import printable
from typing import Any, Iterable, Union, Optional


class Headers(dict):
    @staticmethod
    def _is_string_printable(string: str) -> bool:
        """
        Checks if characters in string are ascii printable characters.

        :param string: some string.
        :return: is string fully of printable ascii characters or not.
        """
        return all(map(lambda char: char in printable, string))

    def __setitem__(self, key: str, value: str) -> None:
        """
        Method that sets new values for headers.

        :param key: key in headers, will be lower cased.
        :param value: value of header.
        :return: nothing.

        :raises ValueError: raised when key or value contain
        some unprintable characters.
        """
        if not (
            self._is_string_printable(key) and
            self._is_string_printable(value)
        ):
            raise ValueError(
                "Headers key or value containing not printable characters"
                " (headers must only contain ascii chars that are printable)."
            )

        lowered_key = key.lower()
        if lowered_key in self.keys():
            self[lowered_key].append(value)

        else:
            super().__setitem__(lowered_key, [value])

    def __getitem__(self, item: str) -> list[str]:
        header_value: list[str] = super().__getitem__(item.lower())
        return header_value

    def get(
        self, key: str, default: Optional[Any] = None
    ) -> Optional[Union[list[str], str, Any]]:
        """
        Gets header values, and in case there's just one header with that name
        gives just the string, not list of strings with one element.

        :param key: header case-insensitive name.
        :param default: allows to set default value to return in case there's no header with
        that name.
        :return: nothing if header isn't found, header single value or list
        of values, if header has multiple values for this header name.
        """
        header_value: Optional[Union[list[str], str]] = super().get(
            key.lower(), default
        )

        if isinstance(header_value, list) and len(header_value) == 1:
            # If we got just 1 header - why bother unpacking the list in code?
            header_value = header_value[0]

        return header_value

    def to_list(self) -> list[Iterable[bytes]]:
        """
        This method encodes headers to how they must be
        given to ASGI server.
        :return: a tuple of tuples with headers key and value,
        all encoded in utf-8.
        """
        headers_list: list[Iterable[bytes]] = []

        for key, value in self.items():
            if isinstance(value, list):
                headers_list.extend(
                    [
                        [key.encode('utf-8'), header_value.encode('utf-8')]
                        for header_value in value
                    ]
                )

            else:
                raise ValueError(
                    f"Unknown type to encode for header: {type(value)}."
                    "Only lists allowed in headers."
                )

        return headers_list

    @classmethod
    def from_list(cls, raw_headers: list[Iterable[bytes]]) -> 'Headers':
        new_headers = cls()
        assert isinstance(raw_headers, list), (
            "ASGI server must give list here"
        )

        for name, value in raw_headers:
            new_headers[name.decode()] = value.decode()

        return new_headers
