from cpython.bytes cimport PyBytes_FromStringAndSize


cdef bytes _fast_b62encode(const uint8_t* src, size_t src_len):
    cdef char[BASE62_ENCODED_LENGTH] dst_buf
    cdef int err_code

    err_code = ksuid_b62_encode(dst_buf, BASE62_ENCODED_LENGTH, src, src_len)

    # Checking error codes
    if err_code != 0:
        if err_code == ERR_B62_INSUFFICIENT_OUTPUT_BUFFER:
            raise ValueError("Insufficient output buffer size")
        elif err_code == ERR_B62_INSUFFICIENT_INPUT_BUFFER:
            raise ValueError("Insufficient input buffer size")
        elif err_code == ERR_B62_INVALID_INPUT:
            raise ValueError("Invalid input buffer")
        else:
            raise ValueError("Unknown error: %d" % err_code)  # pragma: no cover

    return PyBytes_FromStringAndSize(dst_buf, BASE62_ENCODED_LENGTH)


cdef bytes _fast_b62decode(const char* src, size_t src_len):
    cdef unsigned char[BASE62_BYTE_LENGTH] dst_buf
    cdef int err_code

    err_code = ksuid_b62_decode(dst_buf, BASE62_BYTE_LENGTH, src, src_len)

    # Checking error codes
    if err_code != 0:
        if err_code == ERR_B62_INSUFFICIENT_OUTPUT_BUFFER:
            raise ValueError("Insufficient output buffer size")
        elif err_code == ERR_B62_INSUFFICIENT_INPUT_BUFFER:
            raise ValueError("Insufficient input buffer size")
        elif err_code == ERR_B62_INVALID_INPUT:
            raise ValueError("Invalid input buffer")
        else:
            raise ValueError("Unknown error: %d" % err_code)  # pragma: no cover

    return PyBytes_FromStringAndSize(<char *>dst_buf, BASE62_BYTE_LENGTH)


def fast_b62encode(bytes src):
    return _fast_b62encode(src, len(src))


def fast_b62decode(bytes src):
    return _fast_b62decode(src, len(src))
