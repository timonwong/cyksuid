from libc.stdint cimport *


cdef extern from "cbase62.h" nogil:
    int ksuid_b62_encode(char *dst, size_t dst_len, const unsigned char *src, size_t src_len)
    int ksuid_b62_decode(unsigned char *dst, size_t dst_len, const char *src, size_t src_len)


cdef bytes _fast_b62encode(const uint8_t* src, size_t src_len)
cdef bytes _fast_b62decode(const char* src, size_t src_len)
