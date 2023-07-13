.. highlight:: shell

============
Installation
============


Stable release
--------------

To install Hetzner Cloud Python, run this command in your terminal:

.. code-block:: console

    $ pip install hcloud

This is the preferred method to install Hetzner Cloud Python, as it will always install the most recent stable release.

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/


Via conda (Third-Party)
-----------------------

Hetzner Cloud Python is also available as a ``conda``-package via `conda-forge`. This package is not maintained by Hetzner Cloud and might be outdated._:

.. code-block:: console

    $ conda install -c conda-forge hcloud

.. _conda-forge: https://conda-forge.org/


From sources
------------

The sources for Hetzner Cloud Python can be downloaded from the Github repo.

You can either clone the public repository:

.. code-block:: console

    $ git clone git://github.com/hetznercloud/hcloud-python

Or download the tarball:

.. code-block:: console

    $ curl  -OL https://github.com/hetznercloud/hcloud-python/tarball/main

Once you have a copy of the source, you can install it with:

.. code-block:: console

    $ pip install .
