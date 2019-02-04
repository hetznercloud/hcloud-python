Servers
======================


Get all servers
----------------

Get all servers from within the account of the API token.

.. code-block:: python

  #client = HcloudClient(token="Your-Project-Token")
   client.servers.get_all()

**Response:** List[:ref:`server_domain`]

.. list-table::
   :widths: 15 10 10 30
   :header-rows: 1

   * - Parameter
     - Type
     - Description
     - Sample
   * - name
     - string (optional)
     - Can be used to filter servers by their name. The response will only contain the server matching the specified name.
     - `my-server`
   * - label_selector
     - string (optional)
     - Can be used to filter servers by labels. The response will only contain servers matching the label selector. For more details head over to: `Hetzner Cloud API Documentation <https://docs.hetzner.cloud/#overview-label-selector>`_.
     - `k==v`

List all servers
-----------------

List all servers with more granular control over how many servers will be returned.

.. code-block:: python

  #client = HcloudClient(token="Your-Project-Token")
   client.servers.get_list()

**Response:** List[:ref:`server_domain`]

.. list-table::
   :widths: 15 10 10 30
   :header-rows: 1

   * - Parameter
     - Type
     - Description
     - Sample
   * - name
     - string (optional)
     - Can be used to filter servers by their name. The response will only contain the server matching the specified name.
     - `my-server`
   * - label_selector
     - string (optional)
     - Can be used to filter servers by labels. The response will only contain servers matching the label selector. For more details head over to: `Hetzner Cloud API Documentation <https://docs.hetzner.cloud/#overview-label-selector>`_.
     - `k==v`
   * - page
     - string (optional)
     - Get all servers listed at a specific page.
     - `1`
   * - per_page
     - string (optional)
     - Specify the number of servers listed per page. Default: `25` Max: `50`
     - `25`

Create a server
-----------------

Creates a new server. Returns preliminary information about the server as well as an action that covers progress of creation.

.. code-block:: python

  #client = HcloudClient(token="Your-Project-Token")
   client.servers.create()

**Response:** :ref:`server_create_response_domain`


.. list-table::
   :widths: 15 10 10 30
   :header-rows: 1

   * - Parameter
     - Type
     - Description
     - Sample
   * - name
     - string
     - Name of the server to create
     - `my-server`
   * - server_type
     - :ref:`server_type_domain`
     - Server Type
     - -
   * - page
     - string (optional)
     - Get all servers listed at a specific page.
     - `1`
   * - per_page
     - string (optional)
     - Specify the number of servers listed per page. Default: `25` Max: `50`
     - `25`
