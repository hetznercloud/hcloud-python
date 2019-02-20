Hetzner Cloud Python
====================


.. image:: https://travis-ci.com/hetznercloud/hcloud-python.svg?branch=master
    :target: https://travis-ci.com/hetznercloud/hcloud-python
  
    
**IMPORTANT: This project is still in development and not ready production yet!**

Official Hetzner Cloud python library


* Free software: MIT license
* Documentation: https://hcloud-python.readthedocs.io.
* API Reference: https://docs.hetzner.cloud.


Setup Dev environment
---------------------
1) `mkvirtualenv hcloud-python`

2) `pip install -e .` or `pip install -e .[docs]` to be able to build docs


Run tests
---------
* `tox .`
* You can specify environment e.g `tox -e py36`



Create Documentation
--------------------

Run `make docs`. This will also open a documentation in a tab in your default browser. 


Usage example
------------- 

After the documentation has been created, click on `Usage` section

Or open `docs/usage.rst`

You can find some more examples under `examples/`.


Style Guide
-------------
* **Type Hints**: If the type hint line is too long use inline hinting. Maximum inline type hint line should be 150 chars.