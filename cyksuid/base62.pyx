from libc.math cimport log
from libc.stdlib cimport ldiv_t, ldiv
from libc.string cimport memset
from cpython.mem cimport PyMem_Malloc, PyMem_Free
from cpython.bytes cimport PyBytes_FromStringAndSize



cdef u8* table_b2a_base62 = <u8*>b"0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

cdef i8[128] table_a2b_base62 = [
    -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
    -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
    -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
     0,  1,  2,  3,  4,  5,  6,  7,  8,  9, -1, -1, -1, -1, -1, -1,
    -1, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24,
    25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, -1, -1, -1, -1, -1,
    -1, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50,
    51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, -1, -1, -1, -1, -1,
]


cdef inline size_t conversion_len_bound(size_t length, size_t src_base, size_t dst_base):
    cdef double out = <double>length * log(<double>src_base) / log(<double>dst_base)
    return <size_t>out + 1


# Change the base of a byte string representing a big-endian encoded arbitrary-size unsigned integer.
cdef size_t change_base(u8[] dst, size_t dst_len, u8[] src, size_t src_len, size_t src_base, size_t dst_base):
    cdef size_t i
    cdef ldiv_t quot_rem
    cdef long int acc

    cdef size_t off = dst_len
    cdef size_t num_len = src_len

    while num_len > 0:
        i = 0
        quot_rem.quot = quot_rem.rem = 0

        for j in range(num_len):
            acc = quot_rem.rem * src_base + src[j]
            quot_rem = ldiv(acc, dst_base)

            if i != 0 or quot_rem.quot != 0:
                src[i] = <u8>quot_rem.quot
                i += 1

        off -= 1
        dst[off] = <u8>quot_rem.rem
        num_len = i

    return off


cdef inline size_t encode_raw(u8[] dst, size_t dst_len, u8[] src, size_t src_len):
    cdef size_t off = change_base(dst, dst_len, src, src_len, 256, 62)

    for i in range(dst_len):
        dst[i] = table_b2a_base62[dst[i]]

    return off


cdef inline size_t decode_raw(u8[] dst, size_t dst_len, u8[] src, size_t src_len):
    # Map each ascii-encoded Base62 character to its binary value.
    cdef u8 ch
    cdef i8 b

    for i in range(src_len):
        ch = <u8>src[i]
        if ch & 0x80 != 0:
            raise ValueError("non-ascii character in src")

        b = table_a2b_base62[ch]
        if b < 0:
            raise ValueError("invalid base62 character in src")

        src[i] = b

    return change_base(dst, dst_len, src, src_len, 62, 256)


cpdef bytes b62encode(bytes s):
    cdef bytearray src = bytearray(s)
    cdef size_t dst_len = conversion_len_bound(len(s), 256, 62)
    cdef u8* dst = <u8*>PyMem_Malloc(dst_len)
    if not dst:
        raise MemoryError()

    memset(dst, 0, dst_len)
    try:
        encode_raw(dst, dst_len, src, len(src))
        return PyBytes_FromStringAndSize(<char *>dst, dst_len)
    finally:
        PyMem_Free(dst)


cpdef bytes b62decode(bytes s):
    cdef size_t off
    cdef bytearray src = bytearray(s)
    cdef size_t dst_len = conversion_len_bound(len(s), 62, 256)
    cdef u8* dst = <u8*>PyMem_Malloc(dst_len)
    if not dst :
        raise MemoryError()

    memset(dst, 0, dst_len)
    try:
        # We do not need padding while decoding
        off = decode_raw(dst, dst_len, src, len(src))
        return PyBytes_FromStringAndSize(<char *>&dst[off], dst_len - off)
    finally:
        PyMem_Free(dst)
