from cyksuid._ksuid import Empty, Ksuid, Ksuid48, KsuidSvix, ksuid, parse


def from_bytes(raw: bytes) -> Ksuid:
    return Ksuid(raw)


__all__ = ["from_bytes", "ksuid", "parse", "Empty", "Ksuid", "KsuidSvix", "Ksuid48"]
