Server Actions
======================

Power on a server
-----------------

Starts a server by turning its power on.

.. code-block:: python

  #client = HcloudClient(token="Your-Project-Token")
  #server = client.servers.get_by_id(123)
   server.power_on()

**Response:** :ref:`action_domain`

Power off a server
-----------------

Cuts power to the server

.. code-block:: python

  #client = HcloudClient(token="Your-Project-Token")
  #server = client.servers.get_by_id(123)
   server.power_off()

**Response:** :ref:`action_domain`

Reboot a server
-----------------

Reboots a server gracefully by sending an ACPI request.

.. code-block:: python

  #client = HcloudClient(token="Your-Project-Token")
  #server = client.servers.get_by_id(123)
   server.reboot()

**Response:** :ref:`action_domain`

Reset a server
-----------------

Cuts power to a server and starts it again.

.. code-block:: python

  #client = HcloudClient(token="Your-Project-Token")
  #server = client.servers.get_by_id(123)
   server.reset()

**Response:** :ref:`action_domain`

Shutdown a server
-----------------

Shuts down a server gracefully by sending an ACPI shutdown request.

.. code-block:: python

  #client = HcloudClient(token="Your-Project-Token")
  #server = client.servers.get_by_id(123)
   server.shutdown()

**Response:** :ref:`action_domain`

Reset root password of a server
-----------------

Resets the root password.

.. code-block:: python

  #client = HcloudClient(token="Your-Project-Token")
  #server = client.servers.get_by_id(123)
   server.reset_password()

**Response:** :ref:`server_reset_root_password_response_domain`

Enable Rescue Mode for a server
-----------------

Enable the Hetzner Rescue System for this server.

.. code-block:: python

  #client = HcloudClient(token="Your-Project-Token")
  #server = client.servers.get_by_id(123)
   server.enable_rescue()

**Response:** :ref:`server_reset_root_password_response_domain`

.. list-table::
   :widths: 15 10 10 30
   :header-rows: 1

   * - Parameter
     - Type
     - Description
     - Sample
   * - type
     - string (optional)
     - Type of rescue system to boot
     - `linux64`
   * - ssh_keys
     - List[:ref:`sshkey_domain`] (optional)
     - Array of SSH keys which should be injected into the rescue system.
     - -

Disable Rescue Mode for a server
-----------------

Disables the Hetzner Rescue System for a server.

.. code-block:: python

  #client = HcloudClient(token="Your-Project-Token")
  #server = client.servers.get_by_id(123)
   server.disable_rescue()

**Response:** :ref:`action_domain`

Create Image from a Server
-----------------

Creates an image (snapshot) from a server by copying the contents of its disks.

.. code-block:: python

  #client = HcloudClient(token="Your-Project-Token")
  #server = client.servers.get_by_id(123)
   server.create_image(description="my-image")

**Response:** :ref:`image_create_response_domain`

.. list-table::
   :widths: 15 10 10 30
   :header-rows: 1

   * - Parameter
     - Type
     - Description
     - Sample
   * - description
     - string (optional)
     - Description of the image. If you do not set this we auto-generate one for you.
     - `new-name`
   * - type
     - string (optional)
     - Type of image to create
     - `snapshot`
   * - labels
     - :ref:`labels_domain` (optional)
     - User-defined labels (key-value pairs)
     - -

Rebuild a Server from an Image
-----------------

Rebuilds a server overwriting its disk with the content of an image, thereby destroying all data on the target server.

.. code-block:: python

  #client = HcloudClient(token="Your-Project-Token")
  #server = client.servers.get_by_id(123)
   server.rebuild(image=Image(name="my-image"))

**Response:** :ref:`action_domain`

.. list-table::
   :widths: 15 10 10 30
   :header-rows: 1

   * - Parameter
     - Type
     - Description
     - Sample
   * - image
     - :ref:`image_domain`
     - Image to rebuilt from.
     - -
