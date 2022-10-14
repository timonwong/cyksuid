import os
from datetime import datetime, timezone

from cython.operator cimport dereference
from libc.string cimport memcpy

from cyksuid.fast_base62 cimport (BASE62_BYTE_LENGTH, BASE62_ENCODED_LENGTH,
                                  _fast_b62decode, _fast_b62encode)

BYTE_LENGTH = BASE62_BYTE_LENGTH
STRING_ENCODED_LENGTH = BASE62_ENCODED_LENGTH
# Empty KSUID sequence
EMPTY_BYTES = b'\x00' * BASE62_BYTE_LENGTH
# A bytes-encoded maximum value for a KSUID
MAX_ENCODED = b"aWgEPTl1tmebfsQzFP4bxwgy80V"

cdef _urandom = os.urandom

cdef class _KsuidMixin(object):
    BASE62_LENGTH = BASE62_ENCODED_LENGTH

    def __init__(self, *args, **kwargs):
        cdef bytes data
        cdef double ts
        cdef int64_t ts_ms

        if len(args) == 0:
            if len(kwargs) == 0:
                # No param given, generate a random payload
                data = _urandom(self.PAYLOAD_LENGTH_IN_BYTES)
            else:
                data = kwargs["payload"]

            self.uid_.assign_from_payload(data, len(data))
            return
        elif len(args) == 1:
            # only 1 param, assign it from raw
            data = args[0]
            self.uid_.assign(data, len(data))
            return
        elif len(args) == 2:
            # 2 params, assign it from timestamp and payload
            ts = args[0]
            ts_ms = <int64_t>(ts * 1000)
            data = args[1]
            self.uid_.assign(ts_ms, data, len(data))
            return

        raise ValueError("invalid number of arguments")  # pragma: no cover

    @classmethod
    def from_timestamp(cls, timestamp):
        cdef bytes payload = _urandom(cls.PAYLOAD_LENGTH_IN_BYTES)
        return cls(timestamp, payload)

    @classmethod
    def from_payload(cls, payload):
        return cls(payload=payload)

    @classmethod
    def from_timestamp_and_payload(cls, timestamp, payload):
        return cls(timestamp, payload)

    @classmethod
    def from_bytes(cls, raw):
        return cls(raw)

    @property
    def datetime(self):
        """Timestamp portion of the ID as a datetime.datetime object."""
        return datetime.fromtimestamp(self.timestamp, tz=timezone.utc)

    @property
    def timestamp_millis(self):
        """Timestamp portion of the ID in milliseconds."""
        return self.uid_.timestamp_millis()

    @property
    def timestamp(self):
        """Timestamp portion of the ID in seconds."""
        return self.uid_.timestamp_millis() / 1000.0

    @property
    def payload(self):
        """Payload portion of the ID."""
        cdef MemoryView pv = self.uid_.payload()
        return pv.data[:pv.size]

    @property
    def bytes(self):
        """Raw bytes representation of the ID."""
        cdef MemoryView pv = self.uid_.raw()
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
        return not self.uid_.empty()

    def __richcmp__(self, object other, int op):
        if not isinstance(other, _KsuidMixin):
            return NotImplemented

        cdef _KsuidMixin that = <_KsuidMixin>other
        if op == 0:  # <
            return dereference(self.uid_) < dereference(that.uid_)
        elif op == 2:  # ==
            return dereference(self.uid_) == dereference(that.uid_)
        elif op == 4:  # >
            return dereference(that.uid_) < dereference(self.uid_)
        elif op == 1:  # <=
            return dereference(self.uid_) <= dereference(that.uid_)
        elif op == 3:  # !=
            return dereference(self.uid_) != dereference(that.uid_)
        elif op == 5:  # >=
            return dereference(that.uid_) <= dereference(self.uid_)

    def __setattr__(self, name, value):
        raise TypeError('Ksuid objects are immutable')

    def __delattr__(self, name):
        raise TypeError('Ksuid objects are immutable')


cdef class Ksuid(_KsuidMixin):
    PAYLOAD_LENGTH_IN_BYTES = 16
    TIMESTAMP_LENGTH_IN_BYTES = 4

    def __cinit__(self):
        self.uid_ = new _Ksuid()

    def __dealloc__(self):
        del self.uid_


cdef class Ksuid40(_KsuidMixin):
    PAYLOAD_LENGTH_IN_BYTES = 15
    TIMESTAMP_LENGTH_IN_BYTES = 5

    def __cinit__(self):
        self.uid_ = new _Ksuid40()

    def __dealloc__(self):
        del self.uid_


cdef class Ksuid48(_KsuidMixin):
    PAYLOAD_LENGTH_IN_BYTES = 14
    TIMESTAMP_LENGTH_IN_BYTES = 6

    def __cinit__(self):
        self.uid_ = new _Ksuid48()

    def __dealloc__(self):
        del self.uid_


def ksuid(time_func=None, rand_func=None, ksuid_cls=Ksuid):
    """Factory to construct KSUID objects.

    :param callable time_func: function for generating time, defaults to time.time.
    :param callable rand_func: function for generating random bytes, defaults to os.urandom.
    :param callable ksuid_cls: KSUID class, defaults to Ksuid.
    """

    if time_func is None and rand_func is None:
        return ksuid_cls()

    if rand_func is None:
        rand_func = _urandom

    cdef bytes payload = rand_func(ksuid_cls.PAYLOAD_LENGTH_IN_BYTES)
    if time_func is None:
        return ksuid_cls(payload=payload)

    cdef double ts = time_func()
    return ksuid_cls(ts, payload)


def parse(object s, object ksuid_cls=None):
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
Empty = Ksuid(EMPTY_BYTES)
