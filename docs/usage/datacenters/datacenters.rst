Datacenters
======================


Get all datacenters
--------------------
.. code-block:: python

  #client = HcloudClient(token="Your-Project-Token")
   client.datacenters.get_all()

**Return:** List[:ref:`datacenter_domain`]

`API Documentation <#datacenters-get-all-datacenters>`_

.. list-table::
   :widths: 15 10 10 30
   :header-rows: 1

   * - Parameter
     - Type
     - Description
     - Sample
   * - name
     - string (optional)
     - Can be used to filter datacenters by their name.
     - `fsn1-dc14`

List datacenters
-----------------

List datacenters with more granular control over how many datacenters will be returned.

.. code-block:: python

  #client = HcloudClient(token="Your-Project-Token")
   client.datacenters.get_list()

**Return:** List[:ref:`datacenter_domain`]

`API Documentation <https://docs.hetzner.cloud/#datacenters-get-all-datacenters>`_

.. list-table::
   :widths: 15 10 10 30
   :header-rows: 1

   * - Parameter
     - Type
     - Description
     - Sample
   * - name
     - string (optional)
     - Can be used to filter datacenters by their name.
     - `fsn1-dc14`
   * - page
     - string (optional)
     - Get all servers listed at a specific page.
     - `1`
   * - per_page
     - string (optional)
     - Specify the number of servers listed per page. Default: `25` Max: `50`
     - `25`

Get a datacenter
-----------------

.. code-block:: python

  #client = HcloudClient(token="Your-Project-Token")
   client.datacenters.get_by_id(id=123)

**Return:** :ref:`datacenter_domain`]

`API Documentation <https://docs.hetzner.cloud/#datacenters-get-a-datacenter>`_
