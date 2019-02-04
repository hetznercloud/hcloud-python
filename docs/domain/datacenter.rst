.. _datacenter_domain:

Datacenter Domain
******************

.. code-block:: python

    from hcloud.datacenters.client import BoundDatacenter


.. list-table:: Properties
   :widths: 15 15 10 10
   :header-rows: 1

   * - Property
     - Type
     - Description
     - Sample
   * - id
     - int
     - ID of the datacenter
     - `123`
   * - name
     - str
     - Unique identifier of the datacenter
     - `fsn1-dc14`
   * - description
     - str
     - Description of the datacenter
     - `Falkenstein 1 DC 14`
   * - location
     - :ref:`location_domain`
     - Location where the datacenter resides in
     - -
   * - server_types
     - tuple
     - The server types the datacenter can handle
     - -