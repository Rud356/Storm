from typing import Iterable

from string import printable


class Headers(dict):
    @staticmethod
    def is_string_printable(string: str) -> bool:
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

        :raises AssertionError: raised when key or value contain
        some unprintable characters. Works only when run without -O flag.
        """
        assert (
            self.is_string_printable(key) and
            self.is_string_printable(value)
        ), (
            "Headers key or value containing not printable characters"
            " (headers must only contain ascii chars that are printable)."
        )
        lowered_key = key.lower()
        if lowered_key in self.keys():
            self[lowered_key].append(value)

        else:
            super().__setitem__(lowered_key, [value])

    def __getitem__(self, item: str) -> list[str]:
        return super().__getitem__(item.lower())

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
