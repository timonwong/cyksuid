from ksuid import Ksuid
from cyksuid import ksuid


def test_cyksuid(benchmark):
    benchmark(ksuid.ksuid)


def test_svix_ksuid(benchmark):
    benchmark(Ksuid)
