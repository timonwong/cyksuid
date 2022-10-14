"""Compatibility layer."""

from datetime import datetime
from typing import Optional

from cyksuid import hints
from cyksuid._ksuid import (
    BYTE_LENGTH,
    EMPTY_BYTES,
    MAX_ENCODED,
    STRING_ENCODED_LENGTH,
    Empty,
    Ksuid,
)
from cyksuid._ksuid import ksuid as _new_ksuid
from cyksuid._ksuid import parse as _new_parse


class KSUID(Ksuid):
    """KSUIDs are 20 bytes contains 4 byte timestamp with custom epoch and 16 bytes random data."""

    @property
    def timestamp(self) -> int:
        """Timestamp in seconds."""
        return super().timestamp_millis // 1000

    @property
    def datetime(self) -> datetime:
        """Datetime for timestamp (timezone naive)."""
        return datetime.utcfromtimestamp(self.timestamp)


def from_bytes(raw: hints.Bytes) -> KSUID:
    """Construct KSUID from raw bytes."""
    return KSUID(raw)


def parse(s: hints.StrOrBytes) -> KSUID:
    """Parse KSUID from base62 encoded form."""
    return _new_parse(s, ksuid_cls=KSUID)


def ksuid(
    time_func: Optional[hints.TimeFunc] = None,
    rand_func: Optional[hints.RandFunc] = None,
) -> KSUID:
    """Factory to construct KSUID objects.

    :param callable time_func: function for generating time, defaults to time.time.
    :param callable rand_func: function for generating random bytes, defaults to os.urandom.
    """
    return _new_ksuid(time_func=time_func, rand_func=rand_func, ksuid_cls=KSUID)


__all__ = [
    "BYTE_LENGTH",
    "STRING_ENCODED_LENGTH",
    "EMPTY_BYTES",
    "MAX_ENCODED",
    "Empty",
    "Ksuid",
    "parse",
]
