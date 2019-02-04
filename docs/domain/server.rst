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
     - tuple
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
     - str, null
     - Root password of the server, if no ssh key was given at creation.
     - `YItygq1v3GYjjMomLaKc`

.. _server_reset_root_password_response_domain:

Reset Password Response Domain
******************************

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
     - str, null
     - The new root password
     - `YItygq1v3GYjjMomLaKc`