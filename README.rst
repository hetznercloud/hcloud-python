Hetzner Cloud Python
====================


.. image:: https://travis-ci.com/hetznercloud/hcloud-python.svg?branch=master
    :target: https://travis-ci.com/hetznercloud/hcloud-python
.. image:: https://readthedocs.org/projects/hcloud-python/badge/?version=latest
    :target: https://hcloud-python.readthedocs.io
.. image:: https://img.shields.io/pypi/pyversions/hcloud.svg
    :target: https://pypi.org/project/hcloud/

Official Hetzner Cloud python library

The library's documentation is available at `ReadTheDocs`_, the public API documentation is available at https://docs.hetzner.cloud.

.. _ReadTheDocs: https://hcloud-python.readthedocs.io

Usage example
-------------

After the documentation has been created, click on `Usage` section

Or open `docs/usage.rst`

You can find some more examples under `examples/`.


Development
-----------

Setup Dev Environment
---------------------
1) `mkvirtualenv hcloud-python`

2) `pip install -e .` or `pip install -e .[docs]` to be able to build docs


Run tests
---------
* `tox .`
* You can specify environment e.g `tox -e py36`
* You can test the code style with `tox -e flake8`

Create Documentation
--------------------

Run `make docs`. This will also open a documentation in a tab in your default browser. 


Style Guide
-------------
* **Type Hints**: If the type hint line is too long use inline hinting. Maximum inline type hint line should be 150 chars.

License
-------------
The MIT License (MIT). Please see `License File`_ for more information.

.. _License File: https://github.com/hetznercloud/hcloud-python/blob/master/LICENSE
