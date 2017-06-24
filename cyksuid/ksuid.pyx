import binascii
import datetime
import os
import struct
import time

from cyksuid cimport base62

from libc.string cimport memset
from cpython.version cimport PY_MAJOR_VERSION
from cpython.bytes cimport PyBytes_FromStringAndSize

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

    @property
    def datetime(self):
        """Returns timestamp portion of the ID as a datetime.datetime object."""
        ts = self.timestamp
        return datetime.datetime.utcfromtimestamp(ts + _EPOCH_STAMP)

    @property
    def timestamp(self):
        return struct.unpack('>i', self._bytes[:_TIMESTAMP_LENGTH])[0]

    @property
    def payload(self):
        return self._bytes[:_BODY_LENGTH]

    @property
    def bytes(self):
        return self._bytes

    @property
    def hex(self):
        return binascii.b2a_hex(self._bytes)

    @property
    def encoded(self):
        return _to_encoded(self._data)

    def __hash__(self):
        return hash(self._data)

    def __repr__(self):
        return 'KSUID(%r)' % str(self)

    def __str__(self):
        s = _to_encoded(self._data)
        if PY_MAJOR_VERSION >= 3:
            return s.decode('ascii')
        return s

    def __len__(self):
        return len(self._data)

    def __richcmp__(KSUID self, object other, int op):
        if not isinstance(other, KSUID):
            return NotImplemented
        if op == 0:  # <
            return self.bytes < other.bytes
        elif op == 2:  # ==
            return self.bytes == other.bytes
        elif op == 4:  # >
            return self.bytes > other.bytes
        elif op == 1:  # <=
            return self.bytes <= other.bytes
        elif op == 3:  # !=
            return self.bytes != other.bytes
        elif op == 5:  # >=
            return self.bytes >= other.bytes

    def __setattr__(self, name, value):
        raise TypeError('KSUID objects are immutable')

    def __delattr__(self, name):
        raise TypeError('KSUID objects are immutable')



cdef inline bytes _to_encoded(bytes data):
    cdef bytearray src = bytearray(data)
    cdef unsigned char[_STRING_ENCODED_LENGTH] dst

    memset(dst, 0, _STRING_ENCODED_LENGTH)
    base62.encode_raw(dst, _STRING_ENCODED_LENGTH, src, len(src))
    decoded = PyBytes_FromStringAndSize(<char *>dst, _STRING_ENCODED_LENGTH)
    return decoded


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

    cdef bytearray src = bytearray(s)
    cdef unsigned char[_BYTE_LENGTH] dst

    memset(dst, 0, _BYTE_LENGTH)
    base62.decode_raw(dst, _BYTE_LENGTH, src, len(src))
    cdef bytes decoded = PyBytes_FromStringAndSize(<char *>dst, _BYTE_LENGTH)

    return from_bytes(decoded)


# Represents a completely empty (invalid) KSUID
Empty = KSUID(b'')
