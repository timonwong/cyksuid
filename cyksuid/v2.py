from cyksuid import hints
from cyksuid._ksuid import (
    BYTE_LENGTH,
    EMPTY_BYTES,
    STRING_ENCODED_LENGTH,
    MAX_ENCODED,
    Empty,
    Ksuid,
    Ksuid40,
    Ksuid48,
    ksuid,
    parse,
)


def from_bytes(raw: hints.Bytes) -> Ksuid:
    """Create a new KSUID from raw bytes."""
    return Ksuid(raw)


KsuidMs = Ksuid40

__all__ = [
    "BYTE_LENGTH",
    "EMPTY_BYTES",
    "STRING_ENCODED_LENGTH",
    "MAX_ENCODED",
    "from_bytes",
    "ksuid",
    "parse",
    "Empty",
    "Ksuid",
    "Ksuid40",
    "KsuidMs",
    "Ksuid48",
]
