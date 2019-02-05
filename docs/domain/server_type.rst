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
     - ID of server type
     - `123`
   * - name
     - str
     - 	Unique identifier of the server type
     - `cx11`
   * - status
     - str
     - Status of the server
     - `running`
   * - description
     - str
     - Description of the server type
     - `CX11`
   * - cores
     - int
     - Number of cpu cores a server of this type will have
     - `1`
   * - memory
     - int
     - Memory a server of this type will have in GB
     - `1`
   * - disk
     - int
     - Disk size a server of this type will have in GB
     - `25`
   * - prices
     - List
     - Prices in different Locations
     - -
   * - storage_type
     - str
     - Type of server boot drive
     - `local`
   * - storage_type
     - str
     - Type of cpu
     - `shared`

You can find more information about this resource in our `API Documentation <https://docs.hetzner.cloud/#server-types>`_.