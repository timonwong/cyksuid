import datetime
import time

import pytest

from cyksuid import ksuid


def test_construct_from_timestamp() -> None:
    cur_time = time.time()

    def time_func() -> float:
        return cur_time

    x = ksuid.ksuid(time_func=time_func)
    assert x.datetime == datetime.datetime.utcfromtimestamp(int(cur_time))


def test_empty() -> None:
    assert not bool(ksuid.Empty)
    x = ksuid.from_bytes(b"\x00" * ksuid.BYTE_LENGTH)
    assert x == ksuid.Empty


def test_encoding() -> None:
    x = ksuid.from_bytes(b"\x00" * ksuid.BYTE_LENGTH)
    assert not x, "Zero-byte array should be empty!"
    encoded = x.encoded
    assert encoded == b"0" * ksuid.STRING_ENCODED_LENGTH


def test_padding() -> None:
    x = ksuid.from_bytes(b"\xff" * ksuid.BYTE_LENGTH)
    x_encoded = x.bytes
    empty_encoded = ksuid.Empty.bytes
    assert len(x_encoded) == len(
        empty_encoded
    ), "Encoding should produce equal-length strings for zero and max case"


def test_parse() -> None:
    with pytest.raises(TypeError):
        ksuid.parse(b"123")

    parsed = ksuid.parse(b"0" * ksuid.STRING_ENCODED_LENGTH)
    assert parsed == ksuid.Empty

    parsed = ksuid.parse("0" * ksuid.STRING_ENCODED_LENGTH)
    assert parsed == ksuid.Empty

    max_bytes_ksuid = ksuid.from_bytes(b"\xff" * ksuid.BYTE_LENGTH)
    max_parse_ksuid = ksuid.parse(ksuid.MAX_ENCODED)

    assert max_bytes_ksuid == max_parse_ksuid


def test_encode_and_decode() -> None:
    x = ksuid.ksuid()
    build_from_string = ksuid.parse(x.encoded)
    assert x == build_from_string


def dummy_rand_func(n: int) -> bytes:
    return b"\x11" * n


def test_ordering() -> None:
    cur_time = time.time()
    x1 = ksuid.ksuid(time_func=lambda: cur_time, rand_func=dummy_rand_func)
    x2 = ksuid.ksuid(time_func=lambda: cur_time + 1, rand_func=dummy_rand_func)
    assert x2 > x1
    assert x2 >= x1
    assert x1 < x2
    assert x1 <= x2

    x3 = ksuid.ksuid(time_func=lambda: cur_time, rand_func=dummy_rand_func)
    assert x1 == x3
    assert x2 > x3


def test_string_methods() -> None:
    x = ksuid.ksuid(time_func=lambda: 1601693907, rand_func=dummy_rand_func)
    assert str(x) == "1iLjkFPvDHNs6h5VYEZXhMmSaWX"
    assert repr(x) == "KSUID('1iLjkFPvDHNs6h5VYEZXhMmSaWX')"
    assert x.hex == '0c059ad311111111111111111111111111111111'


def test_issue_10() -> None:
    # https://github.com/timonwong/cyksuid/issues/10
    inputs = [
        b"aaaaaaaaaaaaaaaaaaaaaaaaaaa",
        b"aWgEPTl1tmebfsQzFP4bxwgy80!",
    ]
    for s in inputs:
        with pytest.raises(ValueError):
            ksuid.parse(s)
