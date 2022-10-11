from libc.stdint cimport *


cdef extern from "ksuidlite.h" nogil:
    cdef cppclass MemoryView:
        const uint8_t* data
        const size_t size

    cdef cppclass KsuidLite:
        void assign(const uint8_t* data, size_t data_size) except +
        void assign(int64_t ts, const uint8_t* payload, size_t payload_size) except +
        void assign_from_payload(const uint8_t* data, size_t data_size) except +

        int64_t timestamp_millis()
        MemoryView payload()
        MemoryView raw()

        bint empty()
        bint operator<(KsuidLite other)
        bint operator==(KsuidLite other)

    cdef cppclass KsuidImpl[T](KsuidLite):
        KsuidImpl()

    # workaround: https://stackoverflow.com/a/41200186
    cdef cppclass _ks_type_base "4":
        pass
    cdef cppclass _ks_type_svix "5":
        pass
    cdef cppclass _ks_type_48bit "6":
        pass


ctypedef KsuidImpl[_ks_type_base]   _Ksuid
ctypedef KsuidImpl[_ks_type_svix]   _KsuidSvix
ctypedef KsuidImpl[_ks_type_48bit]  _Ksuid48


cdef class _KsuidMixin(object):
    cdef KsuidLite* _uid


cdef class Ksuid(_KsuidMixin):
    """KSUIDs are 20 bytes contains 4 byte timestamp with custom epoch and 16 bytes randomness."""


cdef class KsuidSvix(_KsuidMixin):
    """KSUID compatible with Svix's KSUID implementation."""


cdef class Ksuid48(_KsuidMixin):
    """KSUID with 48 bit timestamp."""


cpdef Ksuid parse(s, object ksuid_cls=*)
