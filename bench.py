import os
import pytest
from ksuid import Ksuid as SvixKsuid

from cyksuid.v2 import ksuid as cy_ksuid
from cyksuid.v2 import parse as cy_parse

TESTS_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "tests")


@pytest.mark.parametrize(
    "gen",
    [
        pytest.param(SvixKsuid, id="svix"),
        pytest.param(cy_ksuid, id="cyksuid"),
    ],
)
def test_generate(benchmark, gen):
    benchmark(gen)


@pytest.mark.parametrize(
    "parse",
    [
        pytest.param(SvixKsuid.from_base62, id="svix"),
        pytest.param(cy_parse, id="cyksuid"),
    ],
)
def test_parse(benchmark, parse):
    benchmark(parse, "Afwp2wWXH1RpvLDMXQkmZtUlWzr")
