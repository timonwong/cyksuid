import functools
from datetime import datetime
from typing import Any, Callable, Optional, Type, TypeVar, overload

_bytestr = bytes

BYTE_LENGTH: int
STRING_ENCODED_LENGTH: int
EMPTY_BYTES: bytes
MAX_ENCODED: bytes

SelfT = TypeVar("SelfT", bound="Ksuid")

@functools.total_ordering
class Ksuid:
    """KSUIDs are 20 bytes contains 4 byte timestamp with custom epoch and 16 bytes random data."""

    BASE62_LENGTH: int
    PAYLOAD_LENGTH_IN_BYTES: int
    TIMESTAMP_LENGTH_IN_BYTES: int

    @overload
    def __init__(self) -> None:
        """Create a new KSUID with current timestamp and generated random payload."""
    @overload
    def __init__(self, raw: bytes) -> None:
        """Creates KSUID from raw bytes."""
    @overload
    def __init__(self, timestamp: int | float, payload: bytes) -> None:
        """Creates KSUID from specified timestamp in milliseconds and payload."""
    @overload
    def __init__(self, **kwargs: Any) -> None: ...
    @classmethod
    def from_payload(cls: Type[SelfT], payload: bytes) -> SelfT: ...
    @classmethod
    def from_timestamp_and_payload(
        cls: Type[SelfT], timestamp: int | float, payload: bytes
    ) -> SelfT: ...
    @classmethod
    def from_bytes(cls: Type[SelfT], raw: bytes) -> SelfT: ...
    def __bool__(self) -> bool: ...
    def __lt__(self, other: object) -> bool: ...
    def __eq__(self, other: object) -> bool: ...
    def __bytes__(self) -> bytes: ...
    @property
    def datetime(self) -> datetime: ...
    @property
    def timestamp_millis(self) -> int: ...
    @property
    def timestamp(self) -> float: ...
    @property
    def payload(self) -> _bytestr: ...
    @property
    def bytes(self) -> _bytestr: ...
    @property
    def hex(self) -> str: ...
    @property
    def encoded(self) -> _bytestr: ...

class Ksuid40(Ksuid):
    """KSUID compatible with 40 bit timestamp, at 4ms precision."""

class Ksuid48(Ksuid):
    """KSUID with 48 bit timestamp."""

TimeFunc = Callable[[], float]
RandFunc = Callable[[int], bytes]

def ksuid(
    time_func: Optional[TimeFunc] = None,
    rand_func: Optional[RandFunc] = None,
    ksuid_cls: Optional[Type[SelfT]] = None,
) -> SelfT:
    """Factory to construct KSUID objects.

    :param time_func: function for generating time, defaults to time.time.
    :param rand_func: function for generating random bytes, defaults to os.urandom.
    :param ksuid_cls: class to use for KSUID, defaults to Ksuid
    """

def parse(s: bytes | str, ksuid_cls: Optional[Type[SelfT]] = None) -> SelfT:
    """Parse KSUID from base62 encoded form."""

# Represents a completely empty (invalid) KSUID
Empty: Ksuid
