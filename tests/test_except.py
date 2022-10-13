import pytest

from cyksuid.v2 import Ksuid, ksuid


def test_ksuids_are_immutable() -> None:
    k: Ksuid = ksuid()
    with pytest.raises(TypeError, match="Ksuid objects are immutable"):
        setattr(k, "timestamp", 10)
    with pytest.raises(TypeError, match="Ksuid objects are immutable"):
        delattr(k, "timestamp")


def test_compare_ksuid_with_other_type() -> None:
    k: Ksuid = ksuid()
    with pytest.raises(TypeError, match="not supported"):
        assert k > 0
