from libc.stdint cimport *


cdef class KSUID(object):
    """KSUIDs are 20 bytes contains 4 byte timestamp with custom epoch and 16 bytes randomness."""
    cdef bytes _bytes
    cdef bytes _data


cpdef KSUID from_bytes(bytes s)
cpdef from_parts(int64_t timestamp, bytes payload)
cpdef KSUID parse(s)
