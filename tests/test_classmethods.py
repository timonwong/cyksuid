import os
import time

from cyksuid.v2 import Ksuid48


def test_from_timestamp() -> None:
    timestamp = time.time()
    k = Ksuid48.from_timestamp(timestamp)
    assert int(k.timestamp) == int(timestamp)


def test_from_payload() -> None:
    timestamp = time.time()
    payload = bytes([i for i in range(Ksuid48.PAYLOAD_LENGTH_IN_BYTES)])
    k = Ksuid48.from_payload(payload)
    assert k.payload == payload
    assert k.timestamp // 10 == timestamp // 10


def test_from_timestamp_and_payload() -> None:
    timestamp = int(time.time() * 1000) / 1000
    payload = os.urandom(Ksuid48.PAYLOAD_LENGTH_IN_BYTES)
    k = Ksuid48.from_timestamp_and_payload(timestamp, payload)
    assert k.payload == payload
    assert k.timestamp == timestamp
