# CyKSUID

A high performance Cython implementation of
[KSUID](https://github.com/segmentio/ksuid) (K-Sortable Globally Unique
IDs).

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
--------------------------------------------------------------------------------------- benchmark 'test_generate': 2 tests ---------------------------------------------------------------------------------------
Name (time in ns)                 Min                    Max                  Mean              StdDev                Median                IQR               Outliers  OPS (Kops/s)            Rounds  Iterations
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
test_generate[cyksuid]       374.9997 (1.0)      16,666.9997 (1.0)        490.1096 (1.0)      127.4882 (1.0)        458.9997 (1.0)      42.0000 (1.0)      13826;14525    2,040.3599 (1.0)      175193           1
test_generate[svix]        1,250.0000 (3.33)     22,290.9998 (1.34)     1,483.5142 (3.03)     796.5151 (6.25)     1,416.0000 (3.08)     42.0000 (1.0)         114;1573      674.0751 (0.33)      13676           1
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

----------------------------------------------------------------------------------------- benchmark 'test_parse': 2 tests -----------------------------------------------------------------------------------------
Name (time in ns)               Min                     Max                   Mean                StdDev                 Median                 IQR            Outliers  OPS (Kops/s)            Rounds  Iterations
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
test_parse[cyksuid]        191.6400 (1.0)        1,250.0000 (1.0)         201.6890 (1.0)         13.9646 (1.0)         200.0000 (1.0)        5.0000 (1.0)     2667;6555    4,958.1283 (1.0)      190477          25
test_parse[svix]        12,042.0000 (62.84)    129,332.9997 (103.47)   12,452.2963 (61.74)    1,232.3979 (88.25)    12,292.0001 (61.46)    125.0000 (25.00)    890;4344       80.3065 (0.02)      28674           1
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
```
