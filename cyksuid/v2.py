from cyksuid._ksuid import Empty, Ksuid, Ksuid48, KsuidSvix, ksuid, parse


def from_bytes(raw: bytes) -> Ksuid:
    """Creates KSUID from raw bytes."""
    return Ksuid(raw)


__all__ = ["from_bytes", "ksuid", "parse", "Empty", "Ksuid", "KsuidSvix", "Ksuid48"]
