from libc.stdint cimport *


cdef enum ERROR_CODE:
    ERR_B62_INSUFFICIENT_OUTPUT_BUFFER = -1
    ERR_B62_INSUFFICIENT_INPUT_BUFFER = -2
    ERR_B62_INVALID_INPUT = -3


cdef enum:
    BASE62_BYTE_LENGTH = 20
    BASE62_ENCODED_LENGTH = 27


cdef extern from "cbase62.h" nogil:
    int ksuid_b62_encode(char *dst, size_t dst_len, const unsigned char *src, size_t src_len)
    int ksuid_b62_decode(unsigned char *dst, size_t dst_len, const char *src, size_t src_len)


cdef bytes _fast_b62encode(const uint8_t* src, size_t src_len)
cdef bytes _fast_b62decode(const char* src, size_t src_len)
