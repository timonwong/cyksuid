import datetime
import os
import time

import cython
from cpython.mem cimport PyMem_Malloc, PyMem_Free
from cython.operator cimport dereference
from libc.string cimport memcpy

from cyksuid.fast_base62 cimport BASE62_BYTE_LENGTH, BASE62_ENCODED_LENGTH
from cyksuid.fast_base62 cimport _fast_b62decode, _fast_b62encode


cdef enum:
    _BODY_LENGTH = 16


BYTE_LENGTH = BASE62_BYTE_LENGTH
STRING_ENCODED_LENGTH = BASE62_ENCODED_LENGTH
# Empty KSUID sequence
EMPTY_BYTES = b'\x00' * BASE62_BYTE_LENGTH
# A bytes-encoded maximum value for a KSUID
MAX_ENCODED = b"aWgEPTl1tmebfsQzFP4bxwgy80V"


@cython.total_ordering
cdef class _KsuidMixin(object):
    def __init__(self, *args, **kwargs):
        cdef bytes data
        cdef int64_t ts

        if len(args) == 0 and len(kwargs) == 0:
            return
        elif len(args) == 1:
            data = args[0]
            self._uid.assign(data, len(data))
            return
        elif len(args) == 2:
            ts = args[0]
            data = args[1]
            self._uid.assign(ts, data, len(data))
            return
        elif len(args) == 0:
            data = kwargs['payload']
            self._uid.assign_from_payload(data, len(data))
            return

        raise ValueError("invalid number of arguments")

    @classmethod
    def from_payload(cls, payload):
        return cls(payload=payload)

    @classmethod
    def from_timestamp_and_payload(cls, timestamp, payload):
        return cls(timestamp, payload)

    @classmethod
    def from_raw(cls, raw):
        return cls(raw)

    @property
    def datetime(self):
        """Timestamp portion of the ID as a datetime.datetime object."""
        cdef double ts = self.timestamp
        return datetime.datetime.utcfromtimestamp(ts)

    @property
    def timestamp_millis(self):
        """Timestamp portion of the ID in milliseconds."""
        return self._uid.timestamp_millis()

    @property
    def timestamp(self):
        """Timestamp portion of the ID in seconds."""
        return self._uid.timestamp_millis() / 1000.0

    @property
    def payload(self):
        """Payload portion of the ID."""
        cdef MemoryView pv = self._uid.payload()
        return pv.data[:pv.size]

    @property
    def bytes(self):
        """Raw bytes representation of the ID."""
        cdef MemoryView pv = self._uid.raw()
        return pv.data[:pv.size]

    @property
    def hex(self):
        """Hex encoded representation of the ID."""
        return self.bytes.hex()

    @property
    def encoded(self):
        """Base62 encoded representation of the ID."""
        cdef bytes b = self.bytes
        return _fast_b62encode(b, len(b))

    def __hash__(self):
        return hash(self.bytes)

    def __bytes__(self):
        return self.bytes

    def __repr__(self):
        return 'KSUID(%r)' % str(self)

    def __str__(self):
        return self.encoded.decode('ascii')

    def __bool__(self):
        return not self._uid.empty()

    def __lt__(self, other):
        if not isinstance(other, Ksuid):
            return NotImplemented

        cdef Ksuid that = <Ksuid>other
        return dereference(self._uid) < dereference(that._uid)

    def __eq__(self, other):
        if not isinstance(other, Ksuid):
            return NotImplemented

        cdef Ksuid that = <Ksuid>other
        return dereference(self._uid) == dereference(that._uid)

    def __setattr__(self, name, value):
        raise TypeError('Ksuid objects are immutable')

    def __delattr__(self, name):
        raise TypeError('Ksuid objects are immutable')


cdef class Ksuid(_KsuidMixin):
    def __cinit__(self):
        self._uid = new _Ksuid()

    def __dealloc__(self):
        del self._uid


cdef class KsuidSvix(_KsuidMixin):
    def __cinit__(self):
        self._uid = new _KsuidSvix()

    def __dealloc__(self):
        del self._uid


cdef class Ksuid48(_KsuidMixin):
    def __cinit__(self):
        self._uid = new _Ksuid48()

    def __dealloc__(self):
        del self._uid


cpdef ksuid(time_func=None, rand_func=None, ksuid_cls=Ksuid):
    """Factory to construct KSUID objects.

    :param callable time_func: function for generating time, defaults to time.time.
    :param callable rand_func: function for generating random bytes, defaults to os.urandom.
    :param callable ksuid_cls: KSUID class, defaults to Ksuid.
    """

    if rand_func is None:
        rand_func = os.urandom

    cdef bytes payload = rand_func(_BODY_LENGTH)

    if time_func is None:
        return ksuid_cls(payload=payload)

    cdef double ts_frac = time_func() * 1000
    cdef int64_t timestamp = <int64_t>int(ts_frac)
    return ksuid_cls(timestamp, payload)


cpdef Ksuid parse(object s, object ksuid_cls=None):
    """Parse KSUID from a base62 encoded string."""

    cdef bytes buf
    if isinstance(s, str):
        buf = (<str>s).encode('utf-8')
    elif isinstance(s, bytes):
        buf = <bytes>s
    else:
        raise TypeError("Expected str or bytes, got %r" % type(s))

    buf_size = len(buf)
    if buf_size != BASE62_ENCODED_LENGTH:
        raise TypeError("invalid encoded KSUID string")

    if not ksuid_cls:
        ksuid_cls = Ksuid
    return ksuid_cls(_fast_b62decode(buf, buf_size))


# Represents a completely empty (invalid) KSUID
Empty = Ksuid()
