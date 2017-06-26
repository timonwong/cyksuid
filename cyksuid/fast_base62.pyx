from cpython.bytes cimport PyBytes_FromStringAndSize

DEF _BASE62_BYTE_LENGTH = 20
DEF _BASE62_ENCODED_LENGTH = 27


cpdef bytes fast_b62encode(bytes src):
    cdef char[_BASE62_ENCODED_LENGTH] dst_buf
    cdef unsigned char * src_buf = src
    cdef int err_code

    err_code = ksuid_b62_encode(dst_buf, _BASE62_ENCODED_LENGTH, src_buf, len(src))

    # Checking error codes
    if err_code == 0:
        pass
    elif err_code == -1:
        raise ValueError("Insufficient output buffer size")
    elif err_code == -2:
        raise ValueError("Insufficient input buffer size")
    elif err_code == -3:
        raise ValueError("Invalid input buffer")
    else:
        raise ValueError("Unknown error: %d" % err_code)

    return PyBytes_FromStringAndSize(dst_buf, _BASE62_ENCODED_LENGTH)


cpdef bytes fast_b62decode(bytes src):
    cdef unsigned char[_BASE62_BYTE_LENGTH] dst_buf
    cdef char * src_buf = src
    cdef int err_code

    err_code = ksuid_b62_decode(dst_buf, _BASE62_BYTE_LENGTH, src_buf, len(src))

    # Checking error codes
    if err_code == 0:
        pass
    elif err_code == -1:
        raise ValueError("Insufficient output buffer size")
    elif err_code == -2:
        raise ValueError("Insufficient input buffer size")
    elif err_code == -3:
        raise ValueError("Invalid input buffer")
    else:
        raise ValueError("Unknown error: %d" % err_code)

    return PyBytes_FromStringAndSize(<char *>dst_buf, _BASE62_BYTE_LENGTH)
