cdef extern from "cbase62.c":
    int ksuid_b62_encode(char *dst, size_t dst_len, const unsigned char *src, size_t src_len) nogil
    int ksuid_b62_decode(unsigned char *dst, size_t dst_len, const char *src, size_t src_len) nogil


cpdef bytes fast_b62encode(bytes src)
cpdef bytes fast_b62decode(bytes src)
