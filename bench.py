from ksuid import Ksuid as SvixKsuid
from cyksuid._ksuid import ksuid as _new_ksuid


def test_cyksuid(benchmark):
    benchmark(_new_ksuid)


def test_svix_ksuid(benchmark):
    benchmark(SvixKsuid)
