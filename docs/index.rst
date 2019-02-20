.. toctree::
   :maxdepth: 4
   :hidden:

   self
   installation
   samples
   api
   Hetzner Cloud API Documentation <https://docs.hetzner.cloud>
   contributing
   changelog

Hetzner Cloud Python
====================


.. image:: https://travis-ci.com/hetznercloud/hcloud-python.svg?branch=master
    :target: https://travis-ci.com/hetznercloud/hcloud-python
.. image:: https://readthedocs.org/projects/hcloud-python/badge/?version=latest
    :target: https://hcloud-python.readthedocs.io


**IMPORTANT: This project is still in development and not ready production yet!**

This is the official `Hetzner Cloud`_ python library.

.. _Hetzner Cloud: https://www.hetzner.com/cloud

Examples
-------------

Create Server
-------------
.. code-block:: python
   :linenos:

   from hcloud import Client
   from hcloud.server_types.domain import ServerType
   from hcloud.images.domain import Image

   client = Client(token="{YOUR_API_TOKEN}")  # Please paste your API token here between the quotes
   response = client.servers.create(name="my-server", server_type=ServerType(name="cx11"), image=Image(name="ubuntu-18.04"))
   server = response.server
   print(server)
   print("Root Password: " + response.root_password)

List Servers
------------
.. code-block:: python
   :linenos:

   from hcloud import Client

   client = Client(token="{YOUR_API_TOKEN}")  # Please paste your API token here between the quotes
   servers = client.servers.get_all()
   print(servers)

You can find more examples in the `Example Folder`_ in the Github Repository.

.. _Example Folder: https://github.com/hetznercloud/hcloud-python/tree/master/examples

License
-------
The MIT License (MIT). Please see `License File`_ for more information.

.. _License File: https://github.com/hetznercloud/hcloud-python/blob/master/LICENSE
