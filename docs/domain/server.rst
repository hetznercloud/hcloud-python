.. _server_domain:

Server Domain
**************

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
     - :ref:`public_network_domain`
     - Public network information
     - -
   * - server_type
     - :ref:`server_type_domain`
     - Type of server
     - -
   * - datacenter
     - :ref:`datacenter_domain`
     - Datacenter this server is located at
     - -
   * - image
     - :ref:`image_domain`, `None`
     - Image this server was created from.
     - -
   * - iso
     - :ref:`iso_domain`, `None`
     - ISO image that is attached to this server. Null if no ISO is attached.
     - -
   * - rescue_enabled
     - boolean
     - 	True if rescue mode is enabled: Server will then boot into rescue system on next reboot.
     - `True`
   * - locked
     - boolean
     - True if server has been locked and is not available to user.
     - `False`
   * - backup_window
     - str, `None`
     - Time window (UTC) in which the backup will run, or `None` if the backups are not enabled
     - `22-02`
   * - outgoing_traffic
     - int, `None`
     - Outbound Traffic for the current billing period in bytes
     - `123456`
   * - ingoing_traffic
     - int, `None`
     - Inbound Traffic for the current billing period in bytes
     - `123456`
   * - included_traffic
     - int
     - Free Traffic for the current billing period in bytes
     - `123456`
   * - protection
     - List[:ref:`protection_domain`]
     - Protection configuration for the server
     - -
   * - labels
     - List[:ref:`labels_domain`]
     - User-defined labels (key-value pairs)
     - -
   * - volumes
     - List[:ref:`volume_domain`]
     - Volumes assigned to this server.
     - -

You can find more information about this resource in our `API Documentation <https://docs.hetzner.cloud/#servers>`_.

.. _public_network_domain:

Public Network Domain
**********************

.. code-block:: python

    from hcloud.servers.domain import PublicNetwork


.. list-table:: Properties
   :widths: 15 15 10 10
   :header-rows: 1

   * - Property
     - Type
     - Description
     - Sample
   * - ipv4
     - :ref:`ipv4_address_domain`
     - ID of server
     - `123`
   * - ivp6
     - :ref:`ipv6_network_domain`
     -
     - `my-server`
   * - floating_ips
     - List[:ref:`floating_ip_domain`]
     - List of Floating IPs which are assigned to the server
     - -

.. _ipv4_address_domain:

IPv4Address Domain
**********************

.. code-block:: python

    from hcloud.servers.domain import IPv4Address


.. list-table:: Properties
   :widths: 15 15 10 10
   :header-rows: 1

   * - Property
     - Type
     - Description
     - Sample
   * - ip
     - str
     - Server IPv4 Address
     - `127.0.0.1`
   * - blocked
     - bool
     - Determine if the IP Address is blocked
     - `False`
   * - dns_ptr
     - str
     - DNS PTR of the IPv4
     - `server01.example.com`

.. _ipv6_network_domain:

IPv6Network Domain
**********************

.. code-block:: python

    from hcloud.servers.domain import IPv6Network


.. list-table:: Properties
   :widths: 15 15 10 10
   :header-rows: 1

   * - Property
     - Type
     - Description
     - Sample
   * - ip
     - str
     - Server IPv6 Network
     - `2001:db8::/64`
   * - blocked
     - bool
     - Determine if the IP Network is blocked
     - `False`
   * - dns_ptr
     - List
     - DNS PTR of all IPv6 Address in the network
     - -

You can find more information about this resource in our `API Documentation <https://docs.hetzner.cloud/#servers>`_.

.. _server_create_response_domain:

Create Server Response Domain
******************************

.. code-block:: python

    from hcloud.servers.domain import CreateServerResponse


.. list-table:: Properties
   :widths: 15 15 10 10
   :header-rows: 1

   * - Property
     - Type
     - Description
     - Sample
   * - server
     - :ref:`server_domain`
     - Created Server
     - -
   * - action
     - :ref:`action_domain`
     - Action that shows the progress of the server creation
     - -
   * - next_actions
     - List[:ref:`action_domain`]
     - additional actions
     - -
   * - root_password
     - str, `None`
     - Root password of the server, if no ssh key was given at creation.
     - `YItygq1v3GYjjMomLaKc`

.. _server_reset_root_password_response_domain:

Reset Password Response Domain
*******************************

.. code-block:: python

    from hcloud.servers.domain import ResetPasswordResponse


.. list-table:: Properties
   :widths: 15 15 10 10
   :header-rows: 1

   * - Property
     - Type
     - Description
     - Sample
   * - action
     - :ref:`action_domain`
     - Action that shows the progress
     - -
   * - root_password
     - str, `None`
     - The new root password
     - `YItygq1v3GYjjMomLaKc`


.. _server_request_console_response_domain:

Request Console Response Domain
********************************

.. code-block:: python

    from hcloud.servers.domain import RequestConsoleResponse


.. list-table:: Properties
   :widths: 15 15 10 10
   :header-rows: 1

   * - Property
     - Type
     - Description
     - Sample
   * - action
     - :ref:`action_domain`
     - Action that shows the progress
     - -
   * - password
     - str
     - VNC password to use for this connection.
     - `YItygq1v3GYjjMomLaKc`
   * - wss_url
     - str
     - URL of websocket proxy to use.
     - `wss://console.hetzner.cloud/?server_id=1&token=3db32d15-af2f-459c-8bf8-dee1fd05f49c`