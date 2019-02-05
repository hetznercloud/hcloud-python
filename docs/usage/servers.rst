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

Get a specific server
-----------------

Returns a specific server object. The server must exist inside the project.

.. code-block:: python

  #client = HcloudClient(token="Your-Project-Token")
   client.servers.get_by_id(1234)

**Response:** :ref:`server_domain`


Create a server
-----------------

Creates a new server. Returns preliminary information about the server as well as an action that covers progress of creation.

.. code-block:: python

  #client = HcloudClient(token="Your-Project-Token")
   client.servers.create(name="my-server", server_type=ServerType(name="cx11"))

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
   * - image
     - :ref:`image_domain`
     - Server Image
     -
   * - location
     - :ref:`location_domain` (optional)
     - Server Location (Specify only one of `location` or `datacenter`)
     - -
   * - datacenter
     - :ref:`datacenter_domain` (optional)
     - Server Datacenter (Specify only one of `location` or `datacenter`)
     - -
   * - ssh_keys
     - List[:ref:`ssh_key_domain`] (optional)
     - SSH keys which should injected into the server at creation time
     - -
   * - volumes
     - List[:ref:`volume_domain`] (optional)
     - Volumes which should attached to the server at creation time
     - -
   * - user_data
     - str (optional)
     - Cloud-Init user data to use during server creation. This field is limited to 32KiB.
     - -
   * - labels
     - List[:ref:`labels_domain`] (optional)
     - User-defined labels (key-value pairs)
     - -
   * - automount
     - boolean (optional)
     - Auto mount volumes after attach.
     - `true`
   * - start_after_create
     - boolean (optional)
     - Start Server right after creation. Defaults to true.
     - `true`


Update a server
-----------------

Updates a server. Returns preliminary information about the server as well as an action that covers progress of creation.

.. code-block:: python

  #client = HcloudClient(token="Your-Project-Token")
  #server = client.servers.get_by_id(123)
   server.update(name="new-name")

**Response:** :ref:`server_domain`


.. list-table::
   :widths: 15 10 10 30
   :header-rows: 1

   * - Parameter
     - Type
     - Description
     - Sample
   * - name
     - string
     - New name to set
     - `new-name`
   * - labels
     - List[:ref:`labels_domain`] (optional)
     - New labels
     - -

Delete a server
-----------------

Deletes a server. This immediately removes the server from your account, and it is no longer accessible.

.. code-block:: python

  #client = HcloudClient(token="Your-Project-Token")
  #server = client.servers.get_by_id(123)
   server.delete()

**Response:** :ref:`action_domain`