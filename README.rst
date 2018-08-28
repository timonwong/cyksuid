CyKSUID
=======

Cython implementation of KSUID_ (K-Sortable Globally Unique IDs).

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

``cyksuid`` supports Python 2.6+ and Python 3.3+ with a common codebase.
It is developed in Cython, but requires no dependecies other than CPython
and a C compiler.

Sample Usage
------------

.. code-block:: python

    from cyksuid import ksuid

    uid = ksuid.ksuid()

    uid.bytes       # b'\x05\xe1\x035\xa8\xbe\xe2\xb5\x0e\x08\xd0\x05\x01L\xe0;\x9a\xed\xc7\xd0'
    uid.hex         # 05e10335a8bee2b50e08d005014ce03b9aedc7d0
    uid.datetime    # datetime.datetime(2017, 6, 28, 6, 48, 21)
    uid.encoded     # b'0q0TPwNTFKyzJKAX1ZRh7rxXiim'
