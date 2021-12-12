from typing import Iterable
from string import printable


class Headers(dict[str, str]):
    @staticmethod
    def is_string_printable(string: str) -> bool:
        """
        Checks if characters in string are ascii printable characters.

        :param string: some string.
        :return: is string fully of printable ascii characters or not.
        """
        return all(map(lambda char: char in printable, string))

    def __setattr__(self, key: str, value: str) -> None:
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
        super().__setattr__(key.lower(), value)

    def to_list(self) -> list[tuple[bytes, bytes]]:
        """
        This method encodes headers to how they must be
        given to ASGI server.
        :return: a tuple of tuples with headers key and value,
        all encoded in utf-8.
        """
        return [
            (key.encode("utf-8"), value.encode("utf-8"))
            for key, value in self.items()
        ]
