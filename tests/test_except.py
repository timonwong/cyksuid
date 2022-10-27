import pytest

from cyksuid.v2 import Ksuid, ksuid, parse


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


def test_parse_with_unsupported_type() -> None:
    with pytest.raises(TypeError, match="Expect str or bytes"):
        parse(0xeeff)  # type: ignore[arg-type]
    with pytest.raises(TypeError, match="Expect str or bytes"):
        parse(1.23)  # type: ignore[arg-type]
