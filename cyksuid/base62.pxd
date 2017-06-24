ctypedef char i8
ctypedef unsigned char u8

# An upper-bound on the length of the result of a generic base conversion.
cdef size_t conversion_len_bound(size_t length, size_t src_base, size_t dst_base)

cdef size_t encode_raw(u8[] dst, size_t dst_len, u8[] src, size_t src_len)

cdef size_t decode_raw(u8[] dst, size_t dst_len, u8[] src, size_t src_len)

cpdef bytes b62encode(bytes s)

cpdef bytes b62decode(bytes s)
