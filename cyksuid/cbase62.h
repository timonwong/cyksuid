#ifndef _CYKSUID_CBASE62_H
#define _CYKSUID_CBASE62_H

#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

int ksuid_b62_encode(char *dst, size_t dst_size, const unsigned char *src, size_t src_size);
int ksuid_b62_decode(unsigned char *dst, size_t dst_size, const char *src, size_t src_size);

#ifdef __cplusplus
}
#endif

#endif /* _CYKSUID_CBASE62_H */
