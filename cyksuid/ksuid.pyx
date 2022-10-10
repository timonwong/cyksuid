import datetime
import os
import time

cimport cython
from cpython.mem cimport PyMem_Malloc, PyMem_Free
from libc.string cimport memcpy

from cyksuid.fast_base62 cimport _fast_b62decode, _fast_b62encode

DEF _BYTE_LENGTH = 20
DEF _STRING_ENCODED_LENGTH = 27
DEF _TIMESTAMP_LENGTH = 4
DEF _BODY_LENGTH = 16
DEF _EPOCH_STAMP = 1400000000

BYTE_LENGTH = _BYTE_LENGTH
STRING_ENCODED_LENGTH = _STRING_ENCODED_LENGTH
# Empty KSUID sequence
EMPTY_BYTES = b'\x00' * _BYTE_LENGTH
# A bytes-encoded maximum value for a KSUID
MAX_ENCODED = b"aWgEPTl1tmebfsQzFP4bxwgy80V"


cdef class KSUID(object):
    def __init__(self, const uint8_t[:] s):
        cdef size_t n = len(s)
        cdef bytes buf
        if s is None or n == 0:
            s = EMPTY_BYTES
        elif n != _BYTE_LENGTH:
            raise TypeError("not a valid ksuid bytes")

        # Remove padding
        cdef int i, start_idx = 0
        with cython.boundscheck(False):
            for i in range(_BYTE_LENGTH):
                if s[i] != 0:
                    break
                start_idx += 1

        self._bytes = bytes(s[:])
        self._data = self._bytes[start_idx:]

    @property
    def datetime(self):
        """Timestamp portion of the ID as a datetime.datetime object."""
        # cdef int64_t ts = <int64_t>self.timestamp
        ts = self.timestamp + _EPOCH_STAMP
        return datetime.datetime.utcfromtimestamp(ts)

    @property
    def timestamp(self):
        """Timestamp portion of the ID in seconds."""
        return int.from_bytes(self._bytes[:_TIMESTAMP_LENGTH], 'big')

    @property
    def payload(self):
        """Payload portion of the ID."""
        return self._bytes[:_BODY_LENGTH]

    @property
    def bytes(self):
        """Raw bytes representation of the ID."""
        return self._bytes

    @property
    def hex(self):
        """Hex encoded representation of the ID."""
        return self._bytes.hex()

    @property
    def encoded(self):
        """Base62 encoded representation of the ID."""
        return _fast_b62encode(self._bytes, len(self._bytes))

    def __hash__(self):
        return hash(self._data)

    def __repr__(self):
        return 'KSUID(%r)' % str(self)

    def __str__(self):
        cdef bytes s = _fast_b62encode(self._bytes, len(self._bytes))
        return s.decode('ascii')

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
            return self._bytes >= that._bytes

    def __setattr__(self, name, value):
        raise TypeError('KSUID objects are immutable')

    def __delattr__(self, name):
        raise TypeError('KSUID objects are immutable')


cpdef KSUID from_bytes(bytes s):
    """Construct KSUID from raw bytes."""
    return KSUID(s)


cpdef KSUID from_parts(int64_t timestamp, bytes payload):
    """Construct KSUID from timestamp."""
    cdef uint32_t ts = <uint32_t>(timestamp - _EPOCH_STAMP)
    cdef size_t payload_len = len(payload)
    cdef size_t buf_size = 4 + payload_len
    cdef uint8_t* buf = <uint8_t *>PyMem_Malloc(buf_size * sizeof(uint8_t))
    if not buf:
        raise MemoryError()

    # big endian representation of ts
    buf[0] = (ts >> 24) & 0xff
    buf[1] = (ts >> 16) & 0xff
    buf[2] = (ts >> 8) & 0xff
    buf[3] = (ts >> 0) & 0xff
    # extend with payload
    memcpy(&buf[4], <const uint8_t*>(payload), payload_len)

    # Convert to bytes, and KSUID
    try:
        return KSUID(buf[:buf_size])
    finally:
        PyMem_Free(buf)


def ksuid(time_func=None, rand_func=None):
    """Factory to construct KSUID objects.

    :param callable time_func: function for generating time, defaults to time.time.
    :param callable rand_func: function for generating random bytes, defaults to os.urandom.
    """
    if time_func is None:
        time_func = time.time
    if rand_func is None:
        rand_func = os.urandom
    cdef int64_t timestamp = <int64_t>int(time_func())
    cdef bytes payload = rand_func(_BODY_LENGTH)
    return from_parts(timestamp, payload)


cpdef KSUID parse(object s):
    """Parse KSUID from a base62 encoded string."""
    cdef bytes buf
    if isinstance(s, str):
        buf = (<str>s).encode('utf-8')
    elif isinstance(s, bytes):
        buf = <bytes>s
    else:
        raise TypeError("Expected str or bytes, got %r" % type(s))

    buf_size = len(buf)
    if buf_size != _STRING_ENCODED_LENGTH:
        raise TypeError("invalid encoded KSUID string")

    return from_bytes(_fast_b62decode(buf, buf_size))


# Represents a completely empty (invalid) KSUID
Empty = KSUID(EMPTY_BYTES)
