Server Actions
======================

List Actions
------------------

Returns a list of action domains for a server.

.. code-block:: python

  #client = HcloudClient(token="Your-Project-Token")
  #server = client.servers.get_by_id(123)
   server.get_actions_list(status=["running"],sort=["id","progress:desc"])

**Return:** List[:ref:`action_domain`]

`API Documentation <https://docs.hetzner.cloud/#server-actions-get-all-actions-for-a-server>`_

.. list-table::
   :widths: 15 10 10 30
   :header-rows: 1

   * - Parameter
     - Type
     - Description
     - Sample
   * - status
     - `List[str]` (optional)
     - Can be used multiple times. Response will have only actions with specified statuses.
     - -
   * - sort
     - `List[str]` (optional)
     - Can be used multiple times.
     - -

Get all Actions
------------------

Returns all action objects for a server.

.. code-block:: python

  #client = HcloudClient(token="Your-Project-Token")
  #server = client.servers.get_by_id(123)
   server.get_actions(status=["running"],sort=["id","progress:desc"])

**Return:** List[:ref:`action_domain`]

`API Documentation <https://docs.hetzner.cloud/#server-actions-get-all-actions-for-a-server>`_

.. list-table::
   :widths: 15 10 10 30
   :header-rows: 1

   * - Parameter
     - Type
     - Description
     - Sample
   * - status
     - `List[str]` (optional)
     - Can be used multiple times. Response will have only actions with specified statuses.
     - -
   * - sort
     - `List[str]` (optional)
     - Can be used multiple times.
     - -

Power on a server
------------------

Starts a server by turning its power on.

.. code-block:: python

  #client = HcloudClient(token="Your-Project-Token")
  #server = client.servers.get_by_id(123)
   server.power_on()

**Return:** :ref:`action_domain`

`API Documentation <https://docs.hetzner.cloud/#server-actions-power-on-a-server>`_

Power off a server
------------------

Cuts power to the server

.. code-block:: python

  #client = HcloudClient(token="Your-Project-Token")
  #server = client.servers.get_by_id(123)
   server.power_off()

**Return:** :ref:`action_domain`

`API Documentation <https://docs.hetzner.cloud/#server-actions-power-off-a-server>`_

Reboot a server
-----------------

Reboots a server gracefully by sending an ACPI request.

.. code-block:: python

  #client = HcloudClient(token="Your-Project-Token")
  #server = client.servers.get_by_id(123)
   server.reboot()

**Return:** :ref:`action_domain`

`API Documentation <https://docs.hetzner.cloud/#server-actions-soft-reboot-a-server>`_

Reset a server
-----------------

Cuts power to a server and starts it again.

.. code-block:: python

  #client = HcloudClient(token="Your-Project-Token")
  #server = client.servers.get_by_id(123)
   server.reset()

**Return:** :ref:`action_domain`

`API Documentation <https://docs.hetzner.cloud/#server-actions-reset-a-server>`_

Shutdown a server
------------------

Shuts down a server gracefully by sending an ACPI shutdown request.

.. code-block:: python

  #client = HcloudClient(token="Your-Project-Token")
  #server = client.servers.get_by_id(123)
   server.shutdown()

**Return:** :ref:`action_domain`

`API Documentation <https://docs.hetzner.cloud/#server-actions-shutdown-a-server>`_

Reset root password of a server
--------------------------------

Resets the root password.

.. code-block:: python

  #client = HcloudClient(token="Your-Project-Token")
  #server = client.servers.get_by_id(123)
   server.reset_password()

**Return:** :ref:`server_reset_root_password_response_domain`

`API Documentation <https://docs.hetzner.cloud/#server-actions-reset-root-password-of-a-server>`_

Enable Rescue Mode for a server
--------------------------------

Enable the Hetzner Rescue System for this server.

.. code-block:: python

  #client = HcloudClient(token="Your-Project-Token")
  #server = client.servers.get_by_id(123)
   server.enable_rescue()

**Return:** :ref:`server_reset_root_password_response_domain`

`API Documentation <https://docs.hetzner.cloud/#server-actions-enable-rescue-mode-for-a-server>`_

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
     - List[:ref:`ssh_key_domain`] (optional)
     - Array of SSH keys which should be injected into the rescue system.
     - -

Disable Rescue Mode for a server
---------------------------------

Disables the Hetzner Rescue System for a server.

.. code-block:: python

  #client = HcloudClient(token="Your-Project-Token")
  #server = client.servers.get_by_id(123)
   server.disable_rescue()

**Return:** :ref:`action_domain`

`API Documentation <https://docs.hetzner.cloud/#server-actions-disable-rescue-mode-for-a-server>`_

Create Image from a Server
---------------------------

Creates an image (snapshot) from a server by copying the contents of its disks.

.. code-block:: python

  #client = HcloudClient(token="Your-Project-Token")
  #server = client.servers.get_by_id(123)
   server.create_image(description="my-image")

**Return:** :ref:`image_create_response_domain`

`API Documentation <https://docs.hetzner.cloud/#server-actions-create-image-from-a-server>`_

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
     - List[:ref:`labels_domain`] (optional)
     - User-defined labels (key-value pairs)
     - -

Rebuild a Server from an Image
-------------------------------

Rebuilds a server overwriting its disk with the content of an image, thereby destroying all data on the target server.

.. code-block:: python

  #client = HcloudClient(token="Your-Project-Token")
  #server = client.servers.get_by_id(123)
   server.rebuild(image=Image(name="my-image"))

**Return:** :ref:`action_domain`

`API Documentation <https://docs.hetzner.cloud/#server-actions-rebuild-a-server-from-an-image>`_

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

Change the Type of a Server
----------------------------

Changes the type (Cores, RAM and disk sizes) of a server.
.. code-block:: python

  #client = HcloudClient(token="Your-Project-Token")
  #server = client.servers.get_by_id(123)
  server.resize(server_type=ServerType(name="cx21"), upgrade_disk=False)

**Return:** :ref:`action_domain`

`API Documentation <https://docs.hetzner.cloud/#server-actions-change-the-type-of-a-server>`_

.. list-table::
   :widths: 15 10 10 30
   :header-rows: 1

   * - Parameter
     - Type
     - Description
     - Sample
   * - server_type
     - :ref:`server_type_domain`
     - Server type the server should migrate to
     - -
   * - upgrade_disk
     - boolean
     - If false, do not upgrade the disk.
     - `False`

Enable Backups for a server
----------------------------

Enables the automatic daily backup option for the server.

.. code-block:: python

  #client = HcloudClient(token="Your-Project-Token")
  #server = client.servers.get_by_id(123)
   server.enable_backup()

**Return:** :ref:`action_domain`

`API Documentation <https://docs.hetzner.cloud/#server-actions-enable-and-configure-backups-for-a-server>`_

Disable Backups for a server
-----------------------------

Disable the automatic daily backup option for the server.

.. code-block:: python

  #client = HcloudClient(token="Your-Project-Token")
  #server = client.servers.get_by_id(123)
   server.disable_backup()

**Return:** :ref:`action_domain`

`API Documentation <https://docs.hetzner.cloud/#server-actions-disable-backups-for-a-server>`_

Attach an ISO to a Server
--------------------------

Attaches an ISO to a server.
.. code-block:: python

  #client = HcloudClient(token="Your-Project-Token")
  #server = client.servers.get_by_id(123)
  server.attach_iso(iso=Iso(name="FreeBSD-11.0-RELEASE-amd64-dvd1"))

**Return:** :ref:`action_domain`

`API Documentation <https://docs.hetzner.cloud/#server-actions-attach-an-iso-to-a-server>`_

.. list-table::
   :widths: 15 10 10 30
   :header-rows: 1

   * - Parameter
     - Type
     - Description
     - Sample
   * - iso
     - :ref:`iso_domain`
     - ISO to attach to the server
     - -

Detach an ISO from a Server
----------------------------

Detaches an ISO from a server.

.. code-block:: python

  #client = HcloudClient(token="Your-Project-Token")
  #server = client.servers.get_by_id(123)
   server.detach_iso()

**Return:** :ref:`action_domain`

`API Documentation <https://docs.hetzner.cloud/#server-actions-detach-an-iso-from-a-server>`_


Change reverse DNS entry for this server
-----------------------------------------

Changes the hostname that will appear when getting the hostname belonging to the primary IPs (ipv4 and ipv6) of this server.

.. code-block:: python

  #client = HcloudClient(token="Your-Project-Token")
  #server = client.servers.get_by_id(123)
   server.change_dns_ptr(ip="1.2.3.4",dns_ptr="server01.example.com")

**Return:** :ref:`action_domain`

`API Documentation <https://docs.hetzner.cloud/#server-actions-change-reverse-dns-entry-for-this-server>`_

.. list-table::
   :widths: 15 10 10 30
   :header-rows: 1

   * - Parameter
     - Type
     - Description
     - Sample
   * - ip
     - str
     - Primary IP address for which the reverse DNS entry should be set.
     - `1.2.3.4`
   * - dns_ptr
     - str, null
     - Hostname to set as a reverse DNS PTR entry. Will reset to original value if `None`
     - `server01.example.com`

Change protection for a Server
-------------------------------

Changes the protection configuration of the server.

.. code-block:: python

  #client = HcloudClient(token="Your-Project-Token")
  #server = client.servers.get_by_id(123)
   server.change_protection(delete=True,rebuild=True)

**Return:** :ref:`action_domain`

`API Documentation <https://docs.hetzner.cloud/#server-actions-change-protection-for-a-server>`_

.. list-table::
   :widths: 15 10 10 30
   :header-rows: 1

   * - Parameter
     - Type
     - Description
     - Sample
   * - delete
     - boolean
     - If true, prevents the server from being deleted (currently delete and rebuild attribute needs to have the same value)
     - `True`
   * - rebuild
     - boolean
     - If true, prevents the server from being rebuilt (currently delete and rebuild attribute needs to have the same value)
     - `True`

Request Console for a Server
-------------------------------

Requests credentials for remote access via vnc over websocket to keyboard, monitor, and mouse for a server.

.. code-block:: python

  #client = HcloudClient(token="Your-Project-Token")
  #server = client.servers.get_by_id(123)
   server.request_console()

**Return:** :ref:`server_request_console_response_domain`

`API Documentation <https://docs.hetzner.cloud/#server-actions-request-console-for-a-server>`_
