Hetzner Cloud Python
====================
**IMPORTANT: This project is still in development and not ready production yet!**

Official Hetzner Cloud python library


* Free software: MIT license
* Documentation: https://hcloud.readthedocs.io.
* API Reference: https://docs.hetzner.cloud.


Setup Dev environment
---------------------
1) `mkvirtualenv hcloud-python`.

2) `pip install -r requirements/dev.txt`.


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

You can find some examples under `examples/`.


Style Guide
-------------
* **Type Hints**: If the type hint line is too long use inline hinting. Maximum inline type hint line should be 150 chars.