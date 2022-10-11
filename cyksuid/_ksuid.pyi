from __future__ import annotations

from datetime import datetime
import functools
from typing import Callable, Optional, Type, TypeVar, overload

_bytestr = bytes

BYTE_LENGTH: int
STRING_ENCODED_LENGTH: int
EMPTY_BYTES: bytes
MAX_ENCODED: bytes

SelfT = TypeVar("SelfT", bound="Ksuid")

@functools.total_ordering
class Ksuid:
    """KSUIDs are 20 bytes contains 4 byte timestamp with custom epoch and 16 bytes randomness."""

    @overload
    def __init__(
        self,
        raw: bytes,
    ) -> None: ...
    @overload
    def __init__(self, timestamp: int, payload: bytes) -> None: ...
    @classmethod
    def from_payload(cls: Type[SelfT], payload: bytes) -> SelfT: ...
    @classmethod
    def from_timestamp_and_payload(
        cls: Type[SelfT], timestamp: int, payload: bytes
    ) -> SelfT: ...
    @classmethod
    def from_raw(cls: Type[SelfT], raw: bytes) -> SelfT: ...
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

class KsuidSvix(Ksuid):
    """KSUID compatible with Svix's KSUID implementation."""

class Ksuid48(Ksuid):
    """KSUID with 48 bit timestamp."""

TimeFunc = Callable[[], float]
RandFunc = Callable[[int], bytes]

def ksuid(
    time_func: Optional[TimeFunc] = None,
    rand_func: Optional[RandFunc] = None,
    ksuid_cls: Optional[Type[SelfT]] = None,
) -> SelfT: ...
def parse(s: bytes | str, ksuid_cls: Optional[Type[SelfT]] = None) -> SelfT: ...

# Represents a completely empty (invalid) KSUID
Empty: Ksuid
