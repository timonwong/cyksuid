# CyKSUID

A high performance Cython implementation of
[KSUID](https://github.com/segmentio/ksuid) (K-Sortable Globally Unique
IDs).

## Badges

![Build Status](https://github.com/timonwong/cyksuid/workflows/Test/badge.svg)
[![Coverage](https://img.shields.io/codecov/c/github/timonwong/cyksuid?token=Nutf41gwoG)](https://app.codecov.io/gh/timonwong/cyksuid)
[![License](https://img.shields.io/github/license/timonwong/cyksuid.svg)](/LICENSE)
[![Release](https://img.shields.io/github/release/timonwong/cyksuid.svg)](https://github.com/timonwong/cyksuid/releases/latest)

## LICENSE

New BSD. See [License
File](https://github.com/timonwong/cyksuid/blob/master/LICENSE).

## Install

`cyksuid` is on the Python Package Index
([PyPI](https://pypi.org/project/cyksuid)):

```bash
pip install cyksuid
```

## Dependencies

`cyksuid` supports Python 3.7+ with a common codebase. It is developed
in Cython, but requires no dependency other than CPython and a C
compiler.

## Sample Usage

### v1 API

```python
from cyksuid import ksuid, parse

uid = ksuid.ksuid()

uid.bytes       # b'\x0f\xd4oB\x81I\xe5\x8d\x95\xb5\xeb\xbc"\xa0\xcd\xfe)N\xe0I'
uid.hex         # '0fd46f428149e58d95b5ebbc22a0cdfe294ee049'
uid.datetime    # datetime.datetime(2022, 10, 12, 13, 12, 34)
uid.timestamp   # 1665580354
uid.encoded     # b'2G2IfS6177qFICE3w10eMjgYu89'

parse(uid.encoded)
```

### v2 API

```python
from cyksuid.v2 import ksuid, parse

uid = ksuid()

uid.bytes       # b'\x0f\xd4oB\x81I\xe5\x8d\x95\xb5\xeb\xbc"\xa0\xcd\xfe)N\xe0I'
uid.hex         # '0fd46f428149e58d95b5ebbc22a0cdfe294ee049'
uid.datetime    # datetime.datetime(2022, 10, 12, 13, 12, 34, tzinfo=datetime.timezone.utc)
uid.timestamp   # 1665580354.0
uid.encoded     # b'2G2IfS6177qFICE3w10eMjgYu89'
str(uid)        # '2G2IfS6177qFICE3w10eMjgYu89'

parse(uid.encoded)
```

## Benchmark

```
platform darwin -- Python 3.11.0, pytest-7.1.3, pluggy-1.0.0
benchmark: 3.4.1 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)

-------------------------------------------------------------------------------------- benchmark 'test_generate': 2 tests -------------------------------------------------------------------------------------
Name (time in ns)                 Min                    Max                  Mean              StdDev                Median                IQR            Outliers  OPS (Kops/s)            Rounds  Iterations
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
test_generate[cyksuid]       292.0278 (1.0)      15,249.9997 (1.0)        438.1552 (1.0)      107.5430 (1.0)        416.9997 (1.0)       0.9895 (1.0)    10589;47969    2,282.2965 (1.0)      137137           1
test_generate[svix]        1,374.9814 (4.71)     27,458.9984 (1.80)     1,504.6515 (3.43)     454.7297 (4.23)     1,458.9750 (3.50)     42.0259 (42.47)     58;1549      664.6057 (0.29)      16316           1
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

--------------------------------------------------------------------------------------- benchmark 'test_parse': 2 tests ----------------------------------------------------------------------------------------
Name (time in ns)               Min                    Max                   Mean              StdDev                 Median                 IQR            Outliers  OPS (Kops/s)            Rounds  Iterations
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
test_parse[cyksuid]        198.3182 (1.0)       1,666.6809 (1.0)         205.4135 (1.0)       14.4218 (1.0)         204.9981 (1.0)        3.3225 (1.0)     1036;5733    4,868.2302 (1.0)      193537          25
test_parse[svix]        10,750.0236 (54.21)    40,624.9892 (24.37)    11,126.0083 (54.16)    624.4237 (43.30)    11,041.9933 (53.86)    124.9718 (37.61)    580;2705       89.8795 (0.02)      30731           1
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Legend:
  Outliers: 1 Standard Deviation from Mean; 1.5 IQR (InterQuartile Range) from 1st Quartile and 3rd Quartile.
  OPS: Operations Per Second, computed as 1 / Mean
============================================================================================ 4 passed in 3.27s =============================================================================================
```
