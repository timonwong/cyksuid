from libc.stdint cimport *


cdef extern from "ksuidlite.h" nogil:
    cdef cppclass MemoryView:
        const uint8_t* data
        const size_t size

    cdef cppclass KsuidLite:
        void assign(const uint8_t*, size_t) except +
        void assign(int64_t, const uint8_t*, size_t) except +
        void assign_from_payload(const uint8_t*, size_t) except +

        int64_t timestamp_millis()
        MemoryView payload()
        MemoryView raw()

        bint empty()
        bint operator<(KsuidLite)
        bint operator<=(KsuidLite)
        bint operator==(KsuidLite)
        bint operator!=(KsuidLite)

    cdef cppclass _Ksuid "Ksuid"(KsuidLite):
        pass

    cdef cppclass _Ksuid40 "Ksuid40"(KsuidLite):
        pass

    cdef cppclass _Ksuid48 "Ksuid48"(KsuidLite):
        pass


cdef class _KsuidMixin(object):
    cdef KsuidLite* uid_


cdef class Ksuid(_KsuidMixin):
    """KSUIDs are 20 bytes contains 4 byte timestamp with custom epoch and 16 bytes randomness."""


cdef class Ksuid40(_KsuidMixin):
    """KSUID compatible with 40 bit timestamp, at 4ms precision."""


cdef class Ksuid48(_KsuidMixin):
    """KSUID with 48 bit timestamp."""


# cpdef Ksuid parse(s, object ksuid_cls=*)
