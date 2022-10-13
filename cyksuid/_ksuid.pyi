import functools
from datetime import datetime
from typing import Any, Callable, Optional, Type, TypeVar, overload

from cyksuid import hints

BYTE_LENGTH: int
STRING_ENCODED_LENGTH: int
EMPTY_BYTES: hints.Bytes
MAX_ENCODED: hints.Bytes

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
    def __init__(self, raw: hints.Bytes) -> None:
        """Create a new KSUID from raw bytes."""
    @overload
    def __init__(self, timestamp: hints.IntOrFloat, payload: hints.Bytes) -> None:
        """Create a new KSUID from specified timestamp in milliseconds and payload."""
    @overload
    def __init__(self, **kwargs: Any) -> None: ...
    @classmethod
    def from_timestamp(cls: Type[SelfT], timestamp: hints.IntOrFloat) -> SelfT:
        """Create a new KSUID with specified timestamp and generated random payload."""
    @classmethod
    def from_payload(cls: Type[SelfT], payload: hints.Bytes) -> SelfT:
        """Create a new KSUID with current timestamp and specified payload."""
    @classmethod
    def from_timestamp_and_payload(
        cls: Type[SelfT], timestamp: hints.IntOrFloat, payload: hints.Bytes
    ) -> SelfT:
        """Create a new KSUID from specified timestamp in milliseconds and payload."""
    @classmethod
    def from_bytes(cls: Type[SelfT], raw: hints.Bytes) -> SelfT:
        """Create a new KSUID from raw bytes."""
    def __bool__(self) -> bool: ...
    def __lt__(self, other: object) -> bool: ...
    def __eq__(self, other: object) -> bool: ...
    def __bytes__(self) -> hints.Bytes: ...
    @property
    def datetime(self) -> datetime:
        """Datetime for timestamp (timezone aware)."""
    @property
    def timestamp_millis(self) -> int:
        """Timestamp in milliseconds."""
    @property
    def timestamp(self) -> float:
        """Timestamp in seconds."""
    @property
    def payload(self) -> hints.Bytes: ...
    @property
    def bytes(self) -> hints.Bytes: ...
    @property
    def hex(self) -> str: ...
    @property
    def encoded(self) -> hints.Bytes:
        """Base62 encoded form of KSUID."""

class Ksuid40(Ksuid):
    """KSUID compatible with 40 bit timestamp, at 4ms precision."""

class Ksuid48(Ksuid):
    """KSUID with 48 bit timestamp."""

def ksuid(
    time_func: Optional[hints.TimeFunc] = None,
    rand_func: Optional[hints.RandFunc] = None,
    ksuid_cls: Optional[Type[SelfT]] = None,
) -> SelfT:
    """Factory to construct KSUID objects.

    :param time_func: function for generating time, defaults to time.time.
    :param rand_func: function for generating random bytes, defaults to os.urandom.
    :param ksuid_cls: class to use for KSUID, defaults to Ksuid
    """

def parse(s: hints.StrOrBytes, ksuid_cls: Optional[Type[SelfT]] = None) -> SelfT:
    """Parse KSUID from base62 encoded form."""

# Represents a completely empty (invalid) KSUID
Empty: Ksuid
