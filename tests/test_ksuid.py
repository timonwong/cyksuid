import json
import os
from datetime import datetime, timedelta, timezone
from typing import Set

import pytest

from cyksuid.v2 import Ksuid, KsuidMs, from_bytes, ksuid, parse

TESTS_DIR = os.path.dirname(os.path.realpath(__file__))

TEST_ITEMS_COUNT = 10
EMPTY_KSUID_PAYLOAD = bytes([0] * Ksuid.PAYLOAD_LENGTH_IN_BYTES)


def test_create() -> None:
    # Arrange
    k: Ksuid = ksuid()
    # Assert
    assert k.timestamp is not None
    assert len(str(k)) == k.BASE62_LENGTH


def test_create_from_timestamp() -> None:
    # Arrange
    now = datetime.now(tz=timezone.utc)
    now_seconds = now.replace(microsecond=0)

    k: Ksuid = ksuid(time_func=lambda: now.timestamp())

    # Assert
    assert k.datetime == now_seconds
    assert k.timestamp == now_seconds.timestamp()


def test_create_from_payload() -> None:
    # Arrange
    payload = os.urandom(Ksuid.PAYLOAD_LENGTH_IN_BYTES)
    ksuid = Ksuid(payload=payload)

    # Assert
    assert ksuid.payload == payload


def test_create_from_payload_and_timestamp() -> None:
    # Arrange
    payload = os.urandom(Ksuid.PAYLOAD_LENGTH_IN_BYTES)
    now = datetime.now(tz=timezone.utc)
    now_seconds = now.replace(microsecond=0)
    ksuid = Ksuid(now.timestamp(), payload)

    # Assert
    assert ksuid.payload == payload
    assert ksuid.datetime == now_seconds
    assert ksuid.timestamp == now_seconds.timestamp()


def test_to_from_base62() -> None:
    # Arrange
    k: Ksuid = ksuid()
    base62 = str(k)

    # Act
    ksuid_from_base62: Ksuid = parse(base62)

    # Assert
    assert k == ksuid_from_base62


def test_to_from_bytes() -> None:
    # Arrange
    k: Ksuid = ksuid()

    # Act
    ksuid_from_bytes = from_bytes(bytes(k))

    # Assert
    assert k == ksuid_from_bytes

    with pytest.raises(ValueError):
        from_bytes(int.to_bytes(10, 2, "big"))


def test_get_payload() -> None:
    # Arrange
    k: Ksuid = ksuid()

    # Assert
    n = Ksuid.TIMESTAMP_LENGTH_IN_BYTES
    assert k.payload == bytes(k)[n:]


def test_compare() -> None:
    # Arrange
    now = datetime.now()
    k: Ksuid = ksuid(time_func=lambda: now.timestamp())
    k_older: Ksuid = ksuid(time_func=lambda: (now - timedelta(hours=1)).timestamp())

    # Assert
    assert k > k_older
    assert not k_older > k
    assert k != k_older
    assert not k == k_older


def test_uniqueness() -> None:
    # Arrange
    ksuids_set: Set[Ksuid] = set()
    for _ in range(TEST_ITEMS_COUNT):
        ksuids_set.add(ksuid())

    # Assert
    assert len(ksuids_set) == TEST_ITEMS_COUNT


def test_payload_uniqueness() -> None:
    # Arrange
    now = datetime.now()
    timestamp = now.replace(microsecond=0).timestamp()
    ksuids_set: Set[Ksuid] = set()
    for i in range(TEST_ITEMS_COUNT):
        ksuids_set.add(ksuid(time_func=lambda: now.timestamp()))

    # Assert
    assert len(ksuids_set) == TEST_ITEMS_COUNT
    for k in ksuids_set:
        assert k.timestamp == timestamp


def test_timestamp_uniqueness() -> None:
    # Arrange
    time = datetime.now()
    ksuids_set: Set[Ksuid] = set()
    for i in range(TEST_ITEMS_COUNT):
        ksuids_set.add(Ksuid(time.timestamp(), EMPTY_KSUID_PAYLOAD))
        time += timedelta(seconds=1)

    # Assert
    assert len(ksuids_set) == TEST_ITEMS_COUNT


def test_ms_mode_datetime() -> None:
    # Arrange
    time = datetime.now()

    def fix_timestamp_precision(timestamp: float) -> float:
        timestamp_ms = int(timestamp * 1000)
        s = timestamp_ms // 1000
        ms = (timestamp_ms % 1000) >> 2
        ms = (ms << 2) % 1000
        return (s * 1000 + ms) / 1000

    for i in range(TEST_ITEMS_COUNT):
        k = ksuid(time_func=lambda: time.timestamp(), ksuid_cls=KsuidMs)
        # Test the values are correct rounded to 4 ms accuracy
        assert fix_timestamp_precision(time.timestamp()) == k.timestamp
        time += timedelta(milliseconds=5)


def test_golib_interop() -> None:
    tf_path = os.path.join(TESTS_DIR, "test_ksuids.txt")

    with open(tf_path, "r") as test_kuids:
        lines = test_kuids.readlines()
        for ksuid_json in lines:
            test_data = json.loads(ksuid_json)
            ksuid = Ksuid(
                test_data["timestamp"],
                bytes.fromhex(test_data["payload"]),
            )
            assert test_data["ksuid"] == str(ksuid)
            ksuid = parse(test_data["ksuid"])
            assert test_data["ksuid"] == str(ksuid)


def test_golib_interop_ms_mode() -> None:
    tf_path = os.path.join(TESTS_DIR, "test_ksuids.txt")

    with open(tf_path, "r") as test_kuids:
        lines = test_kuids.readlines()
        for ksuid_json in lines:
            test_data = json.loads(ksuid_json)
            ksuid = Ksuid(
                test_data["timestamp"],
                bytes.fromhex(test_data["payload"]),
            )
            n = KsuidMs.PAYLOAD_LENGTH_IN_BYTES
            ksuid_ms = KsuidMs(ksuid.datetime.timestamp(), ksuid.payload[:n])
            assert ksuid_ms.datetime == ksuid.datetime
            ksuid_ms_from = KsuidMs(ksuid_ms.datetime.timestamp(), ksuid_ms.payload)
            assert ksuid_ms.payload == ksuid_ms_from.payload
            assert ksuid_ms.timestamp == ksuid_ms_from.timestamp

            ksuid_ms = parse(test_data["ksuid"], ksuid_cls=KsuidMs)
            timediff = ksuid_ms.datetime - ksuid.datetime
            assert abs(timediff.total_seconds() * (10**3)) <= 1000
            assert test_data["ksuid"] == str(ksuid_ms)
