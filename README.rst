CyKSUID
=======

A high performance Cython implementation of KSUID_ (K-Sortable Globally Unique IDs).

.. _KSUID: https://github.com/segmentio/ksuid

LICENSE
-------

New BSD. See `License File <https://github.com/timonwong/cyksuid/blob/master/LICENSE>`__.

Install
-------

``cyksuid`` is on the Python Package Index (`PyPI <https://pypi.org/project/cyksuid>`__):

::

    pip install cyksuid


Dependencies
------------

``cyksuid`` supports Python 3.6+ with a common codebase.
It is developed in Cython, but requires no dependency other than CPython and a C compiler.

Sample Usage
------------

.. code-block:: python

    from cyksuid import ksuid

    uid = ksuid.ksuid()

    uid.bytes       # b'\x05\xe1\x035\xa8\xbe\xe2\xb5\x0e\x08\xd0\x05\x01L\xe0;\x9a\xed\xc7\xd0'
    uid.hex         # 05e10335a8bee2b50e08d005014ce03b9aedc7d0
    uid.datetime    # datetime.datetime(2017, 6, 28, 6, 48, 21)
    uid.encoded     # b'0q0TPwNTFKyzJKAX1ZRh7rxXiim'

Benchmark
---------

::

    -------------------------------------------------------------------------------------------- benchmark: 2 tests -------------------------------------------------------------------------------------------
    Name (time in ns)            Min                    Max                  Mean              StdDev                Median                IQR             Outliers  OPS (Kops/s)            Rounds  Iterations
    -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    test_cyksuid            291.9696 (1.0)      16,166.9450 (1.0)        425.5640 (1.0)      188.1947 (1.0)        416.0684 (1.0)      42.0259 (1.03)     5567;6345    2,349.8230 (1.0)       81355           1
    test_svix_ksuid       1,249.9513 (4.28)     25,499.9613 (1.58)     1,408.5097 (3.31)     243.9162 (1.30)     1,374.9814 (3.30)     40.9782 (1.0)      1297;4647      709.9703 (0.30)      38587           1
    -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
