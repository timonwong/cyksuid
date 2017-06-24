import datetime
import time

import pytest

from cyksuid import ksuid


def test_construct_from_timestamp():
    cur_time = time.time()

    def time_func():
        return cur_time

    x = ksuid.ksuid(time_func=time_func)
    assert x.datetime == datetime.datetime.utcfromtimestamp(int(cur_time))


def test_empty():
    assert not bool(ksuid.Empty)
    x = ksuid.from_bytes(b'\x00' * ksuid.BYTE_LENGTH)
    assert x == ksuid.Empty


def test_encoding():
    x = ksuid.from_bytes(b'\x00' * ksuid.BYTE_LENGTH)
    assert not x, "Zero-byte array should be empty!"
    encoded = x.encoded
    assert encoded == b'0' * ksuid.STRING_ENCODED_LENGTH


def test_padding():
    x = ksuid.from_bytes(b'\xff' * ksuid.BYTE_LENGTH)
    x_encoded = x.bytes
    empty_encoded = ksuid.Empty.bytes
    assert len(x_encoded) == len(empty_encoded), "Encoding should produce equal-length strings for zero and max case"


def test_parse():
    with pytest.raises(TypeError):
        ksuid.parse(b'123')

    parsed = ksuid.parse(b'0' * ksuid.STRING_ENCODED_LENGTH)
    assert parsed == ksuid.Empty

    max_bytes_ksuid = ksuid.from_bytes(b'\xff' * ksuid.BYTE_LENGTH)
    max_parse_ksuid = ksuid.parse(ksuid.MAX_ENCODED)

    assert max_bytes_ksuid == max_parse_ksuid


def test_encode_and_decode():
    x = ksuid.ksuid()
    build_from_string = ksuid.parse(x.encoded)
    assert x == build_from_string


def test_ordering():
    cur_time = time.time()
    x1 = ksuid.ksuid(time_func=lambda: cur_time)
    x2 = ksuid.ksuid(time_func=lambda: cur_time + 1)
    assert x1 < x2

