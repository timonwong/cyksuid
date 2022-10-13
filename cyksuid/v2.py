from cyksuid import hints
from cyksuid._ksuid import Empty, Ksuid, Ksuid40, Ksuid48, ksuid, parse


def from_bytes(raw: hints.Bytes) -> Ksuid:
    """Create a new KSUID from raw bytes."""
    return Ksuid(raw)


KsuidMs = Ksuid40

__all__ = [
    "from_bytes",
    "ksuid",
    "parse",
    "Empty",
    "Ksuid",
    "Ksuid40",
    "KsuidMs",
    "Ksuid48",
]
