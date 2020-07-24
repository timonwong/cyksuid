#include <stddef.h>
#include <string.h>
#include <stdint.h>

// Error Codes
#define ERR_B62_INSUFFICIENT_OUTPUT_BUFFER -1
#define ERR_B62_INSUFFICIENT_INPUT_BUFFER -2
#define ERR_B62_INVALID_INPUT -3

#define _BASE62_BYTE_SIZE 20
#define _BASE62_ENCODED_SIZE 27

static const char table_b2a_base62[] = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";
static const char table_a2b_base62[] = {
    -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
    -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
    -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
    0, 1, 2, 3, 4, 5, 6, 7, 8, 9, -1, -1, -1, -1, -1, -1,
    -1, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24,
    25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, -1, -1, -1, -1, -1,
    -1, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50,
    51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, -1, -1, -1, -1, -1,
};

int ksuid_b62_encode(char *dst, size_t dst_size, const unsigned char *src, size_t src_size) {
    const uint64_t SRC_BASE = 4294967296UL;
    const uint64_t DST_BASE = 62UL;
    size_t i;
    uint32_t *bp;
    size_t bp_len;
    uint32_t bq[5];
    size_t bq_len;
    uint64_t value, digit, rem;
    uint32_t parts[5] = {
        // Bootstrap
        (uint32_t)(src[0]) << 24 | (uint32_t)(src[1]) << 16 | (uint32_t)(src[2]) << 8 | (uint32_t)(src[3]),
        (uint32_t)(src[4]) << 24 | (uint32_t)(src[5]) << 16 | (uint32_t)(src[6]) << 8 | (uint32_t)(src[7]),
        (uint32_t)(src[8]) << 24 | (uint32_t)(src[9]) << 16 | (uint32_t)(src[10]) << 8 | (uint32_t)(src[11]),
        (uint32_t)(src[12]) << 24 | (uint32_t)(src[13]) << 16 | (uint32_t)(src[14]) << 8 | (uint32_t)(src[15]),
        (uint32_t)(src[16]) << 24 | (uint32_t)(src[17]) << 16 | (uint32_t)(src[18]) << 8 | (uint32_t)(src[19]),
    };

    if (src_size != _BASE62_BYTE_SIZE) {
        return ERR_B62_INSUFFICIENT_INPUT_BUFFER;
    }

    if (dst_size != _BASE62_ENCODED_SIZE) {
        return ERR_B62_INSUFFICIENT_OUTPUT_BUFFER;
    }

    bp = parts;
    bp_len = 5;
    while (bp_len) {
        rem = 0;
        bq_len = 0;

        for (i = 0; i < bp_len; i++) {
            value = (uint64_t)bp[i] + rem * SRC_BASE;
            digit = value / DST_BASE;
            rem = value % DST_BASE;

            if (bq_len != 0 || digit != 0) {
                bq[bq_len++] = (uint32_t)digit;
            }
        }

        dst[--dst_size] = table_b2a_base62[rem];
        bp = bq;
        bp_len = bq_len;
    }

    // Add padding at the head of the destination buffer for all bytes that were not set
    if (dst_size) {
        memset(dst, '0', dst_size);
    }

    return 0;
}

int ksuid_b62_decode(unsigned char *dst, size_t dst_size, const char *src, size_t src_size) {
    const uint64_t SRC_BASE = 62UL;
    const uint64_t DST_BASE = 4294967296UL;
    size_t i;
    uint8_t parts[27];
    uint8_t c, v;
    uint8_t *bp;
    size_t bp_len;
    uint8_t bq[27];
    size_t bq_len;
    uint64_t value, digit, rem;

    if (src_size != _BASE62_ENCODED_SIZE) {
        return ERR_B62_INSUFFICIENT_INPUT_BUFFER;
    }

    if (dst_size != _BASE62_BYTE_SIZE) {
        return ERR_B62_INSUFFICIENT_OUTPUT_BUFFER;
    }

    // Bootstrap
    for (i = 0; i < 27; i++) {
        c = src[i];
        v = table_a2b_base62[c & 0x7f];
        if ((c >= 0x80) || (v == (unsigned char)-1)) {
            return ERR_B62_INVALID_INPUT;
        }

        parts[i] = v;
    };

    bp = parts;
    bp_len = 27;
    while (bp_len) {
        rem = 0;
        bq_len = 0;

        for (i = 0; i < bp_len; i++) {
            value = (uint64_t)bp[i] + rem * SRC_BASE;
            digit = value / DST_BASE;
            rem = value % DST_BASE;

            if (bq_len != 0 || digit != 0) {
                bq[bq_len++] = (uint8_t)digit;
            }
        }

        if (dst_size < 4) {
            return ERR_B62_INSUFFICIENT_OUTPUT_BUFFER;
        }

        dst[dst_size - 4] = (uint8_t)(rem >> 24);
        dst[dst_size - 3] = (uint8_t)(rem >> 16);
        dst[dst_size - 2] = (uint8_t)(rem >> 8);
        dst[dst_size - 1] = (uint8_t)(rem);
        dst_size -= 4;
        bp = bq;
        bp_len = bq_len;
    }

    // Add 'zeros' at the head of the destination buffer for all bytes that were not set
    if (dst_size) {
        memset(dst, 0, dst_size);
    }

    return 0;
}
