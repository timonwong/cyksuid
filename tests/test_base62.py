from cyksuid import base62


def test_base10_to_base62_and_back():
    num = b"\x01\x02\x03\x04"
    encoded = base62.b62encode(num)
    decoded = base62.b62decode(encoded)

    assert num == decoded


def test_base256_to_base64_and_back():
    num = b"\255\254\254\251"
    encoded = base62.b62encode(num)
    decoded = base62.b62decode(encoded)

    assert num == decoded


def test_encode_and_decode_base62():
    hello = b"hello, world"
    encoded = base62.b62encode(hello)
    decoded = base62.b62decode(encoded)

    assert hello == decoded


def test_lexicographic_ordering():
    unsorted_strings = []
    for i in range(256):
        b = bytearray((0, i))
        b = bytes(b)
        s = base62.b62encode(b)
        unsorted_strings.append(b'0' * (2 - len(s)) + s)
    unsorted_strings.sort()

    sorted_strings = list(sorted(unsorted_strings))
    assert unsorted_strings == sorted_strings
