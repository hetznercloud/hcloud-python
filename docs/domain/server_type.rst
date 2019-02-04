.. _server_type_domain:

Server Type Domain
*******************

.. code-block:: python

    from hcloud.servers.client import BoundServer


.. list-table:: Properties
   :widths: 15 15 10 10
   :header-rows: 1

   * - Property
     - Type
     - Description
     - Sample
   * - id
     - int
     - ID of server
     - `123`
   * - name
     - str
     - Name of the server
     - `my-server`
   * - status
     - str
     - Status of the server
     - `running`
   * - created
     - str
     - Timestamp when server was created
     - `2016-01-30T23:50+00:00`
   * - public_net
     - tuple
     - Public network information
     - -
   * - server_type
     - tuple
     - Public network information
     - -