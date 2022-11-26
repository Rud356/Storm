import pytest
from storm.types.headers import Headers


def test_headers_parsing():
    header_example: list[list[bytes]] = [
        [b"Content-Length", b"1250"]
    ]
    header = Headers.from_list(header_example)
    assert header == {"content-length": ["1250"]}
    assert header["Content-Length"] == ["1250"]


def test_headers_parsing_with_multivalues():
    header_example: list[list[bytes]] = [
        [b"Some-Header", b"15"],
        [b"Some-Header", b"12"]
    ]
    header = Headers.from_list(header_example)
    assert header["Some-Header"] == ["15", "12"]


def test_headers_get_method():
    header_example: list[list[bytes]] = [
        [b"Content-Length", b"1250"]
    ]
    header = Headers.from_list(header_example)
    assert header == {"content-length": ["1250"]}
    assert header.get("Content-Length") == "1250"

    header_example = [
        [b"Some-Header", b"15"],
        [b"Some-Header", b"12"]
    ]
    header = Headers.from_list(header_example)
    assert header.get("Some-Header") == ["15", "12"]


def test_headers_get_empty():
    with pytest.raises(KeyError):
        assert Headers()["Content-Length"]


def test_headers_get_with_default():
    assert Headers().get("content-length", 123) == 123
