import binascii
import datetime
import os
import struct
import time

from cpython.version cimport PY_MAJOR_VERSION

from cyksuid.fast_base62 cimport fast_b62decode
from cyksuid.fast_base62 cimport fast_b62encode

DEF _BYTE_LENGTH = 20
DEF _STRING_ENCODED_LENGTH = 27
DEF _TIMESTAMP_LENGTH = 4
DEF _BODY_LENGTH = 16
DEF _EPOCH_STAMP = 1400000000

BYTE_LENGTH = _BYTE_LENGTH
STRING_ENCODED_LENGTH = _STRING_ENCODED_LENGTH
# A bytes-encoded maximum value for a KSUID
MAX_ENCODED = b"aWgEPTl1tmebfsQzFP4bxwgy80V"


cdef class KSUID(object):
    cdef bytes _bytes
    cdef bytes _data

    def __init__(self, bytes s):
        if not s:
            s = b'\x00' * _BYTE_LENGTH
        if len(s) != _BYTE_LENGTH:
            raise TypeError("not a valid ksuid bytes")
        self._bytes = s
        # Remove padding
        self._data = s.lstrip(b'\x00')

    property datetime:
        def __get__(self):
            """Returns timestamp portion of the ID as a datetime.datetime object."""
            ts = self.timestamp
            return datetime.datetime.utcfromtimestamp(ts + _EPOCH_STAMP)

    property timestamp:
        def __get__(self):
            return struct.unpack('>i', self._bytes[:_TIMESTAMP_LENGTH])[0]

    property payload:
        def __get__(self):
            return self._bytes[:_BODY_LENGTH]

    property bytes:
        def __get__(self):
            return self._bytes

    property hex:
        def __get__(self):
            return binascii.b2a_hex(self._bytes)

    property encoded:
        def __get__(self):
            return fast_b62encode(self._bytes)

    def __hash__(self):
        return hash(self._data)

    def __repr__(self):
        return 'KSUID(%r)' % str(self)

    def __str__(self):
        s = fast_b62encode(self._bytes)
        if PY_MAJOR_VERSION >= 3:
            return s.decode('ascii')
        return s

    def __len__(self):
        return len(self._data)

    def __richcmp__(KSUID self, object other, int op):
        if not isinstance(other, KSUID):
            return NotImplemented

        cdef KSUID that = <KSUID>other
        if op == 0:  # <
            return self._bytes < that._bytes
        elif op == 2:  # ==
            return self._bytes == that._bytes
        elif op == 4:  # >
            return self._bytes > that._bytes
        elif op == 1:  # <=
            return self._bytes <= that._bytes
        elif op == 3:  # !=
            return self._bytes != that._bytes
        elif op == 5:  # >=
            return self._bytes >= other._bytes

    def __setattr__(self, name, value):
        raise TypeError('KSUID objects are immutable')

    def __delattr__(self, name):
        raise TypeError('KSUID objects are immutable')


def from_bytes(bytes s):
    return KSUID(s)


def from_parts(int timestamp, bytes payload):
    s = struct.pack('>i', timestamp) + payload
    return KSUID(s)


def ksuid(time_func=time.time, rand_fuc=os.urandom):
    timestamp = int(time_func()) - _EPOCH_STAMP
    payload = rand_fuc(_BODY_LENGTH)
    return from_parts(timestamp, payload)


cpdef parse(bytes s):
    if len(s) != _STRING_ENCODED_LENGTH:
        raise TypeError("invalid encoded KSUID string")

    return from_bytes(fast_b62decode(s))


# Represents a completely empty (invalid) KSUID
Empty = KSUID(b'')
