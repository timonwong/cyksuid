from cyksuid.fast_base62 import fast_b62decode, fast_b62encode


def test_convert_and_back() -> None:
    num = b"\x01\x02\x03\x04" * 5

    encoded = fast_b62encode(num)
    decoded = fast_b62decode(encoded)

    assert num == decoded


def test_lexicographic_ordering() -> None:
    unsorted_strings = []
    for i in range(256):
        ba = bytearray((0, i) * 10)
        b = bytes(ba)
        s = fast_b62encode(b)
        unsorted_strings.append(b"0" * (2 - len(s)) + s)
    unsorted_strings.sort()

    sorted_strings = list(sorted(unsorted_strings))
    assert unsorted_strings == sorted_strings
