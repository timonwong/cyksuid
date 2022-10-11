"""Compatibility layer."""

from typing import Callable, Optional
from cyksuid._ksuid import Empty, Ksuid
from cyksuid._ksuid import parse as _new_parse
from cyksuid._ksuid import ksuid as _new_ksuid
from cyksuid._ksuid import BYTE_LENGTH, STRING_ENCODED_LENGTH, EMPTY_BYTES, MAX_ENCODED


class KSUID(Ksuid):
    @property
    def timestamp(self) -> int:
        return super().timestamp_millis // 1000


def from_bytes(raw: bytes) -> KSUID:
    return KSUID(raw)


def parse(s: bytes) -> KSUID:
    return _new_parse(s, ksuid_cls=KSUID)


TimeFunc = Callable[[], float]
RandFunc = Callable[[int], bytes]


def ksuid(
    time_func: Optional[TimeFunc] = None, rand_func: Optional[RandFunc] = None
) -> KSUID:
    """Factory to construct KSUID objects.

    :param callable time_func: function for generating time, defaults to time.time.
    :param callable rand_func: function for generating random bytes, defaults to os.urandom.
    """
    return _new_ksuid(time_func=time_func, rand_func=rand_func, ksuid_cls=KSUID)


__all__ = [
    "Empty",
    "Ksuid",
    "parse",
    "BYTE_LENGTH",
    "STRING_ENCODED_LENGTH",
    "EMPTY_BYTES",
    "MAX_ENCODED",
]
