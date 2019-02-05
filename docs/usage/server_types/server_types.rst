Server Types
======================


Get all Server Types
---------------------

.. code-block:: python

  #client = HcloudClient(token="Your-Project-Token")
   client.server_types.get_all()

**Return:** List[:ref:`server_type_domain`]

`API Documentation <https://docs.hetzner.cloud/#server-types-get-all-server-types>`_

.. list-table::
   :widths: 15 10 10 30
   :header-rows: 1

   * - Parameter
     - Type
     - Description
     - Sample
   * - name
     - string (optional)
     - Can be used to filter locations by their name.
     - `cx11`

List Server Types
------------------

List Server Types with more granular control over how many Server Types will be returned.

.. code-block:: python

  #client = HcloudClient(token="Your-Project-Token")
   client.server_types.get_list()

**Return:** List[:ref:`server_type_domain`]

`API Documentation <https://docs.hetzner.cloud/#server-types-get-all-server-types>`_

.. list-table::
   :widths: 15 10 10 30
   :header-rows: 1

   * - Parameter
     - Type
     - Description
     - Sample
   * - name
     - string (optional)
     - Can be used to filter server types by their name.
     - `cx11`
   * - page
     - string (optional)
     - Get all servers listed at a specific page.
     - `1`
   * - per_page
     - string (optional)
     - Specify the number of servers listed per page. Default: `25` Max: `50`
     - `25`


Get a specific Server Type
---------------------------

.. code-block:: python

  #client = HcloudClient(token="Your-Project-Token")
   client.server_types.get_by_id(id=123)

**Return:** :ref:`server_type_domain`

`API Documentation <https://docs.hetzner.cloud/#server-types-get-a-server-type>`_