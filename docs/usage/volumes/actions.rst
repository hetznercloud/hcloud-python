Volumes Actions
======================

List Actions
------------------

List Actions from the Volume with more granular control over how many Actions will be returned.

.. code-block:: python

  #client = HcloudClient(token="Your-Project-Token")
  #volume = client.volumes.get_by_id(123)
   volume.get_actions_list(status=["running"],sort=["id","progress:desc"])

**Return:** List[:ref:`action_domain`]

`API Documentation <https://docs.hetzner.cloud/#volume-actions-get-all-actions-for-an-volume>`_

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
   * - page
     - string (optional)
     - Get all actions listed at a specific page.
     - `1`
   * - per_page
     - string (optional)
     - Specify the number of actions listed per page. Default: `25` Max: `50`
     - `25`

Get all Actions
------------------

.. code-block:: python

  #client = HcloudClient(token="Your-Project-Token")
  #volume = client.volumes.get_by_id(123)
   volume.get_actions(status=["running"],sort=["id","progress:desc"])

**Return:** List[:ref:`action_domain`]

`API Documentation <https://docs.hetzner.cloud/#volume-actions-get-all-actions-for-an-volume>`_

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

Attach Volume to a Server
-------------------------------

.. code-block:: python

  #client = HcloudClient(token="Your-Project-Token")
  #volume = client.volumes.get_by_id(123)
   volume.attach(server=Server(id=123))

**Return:** :ref:`action_domain`

`API Documentation <https://docs.hetzner.cloud/#volume-actions-attach-volume-to-a-server>`_

.. list-table::
   :widths: 15 10 10 30
   :header-rows: 1

   * - Parameter
     - Type
     - Description
     - Sample
   * - server
     - :ref:`server_domain`
     - Server the volume will be attached to
     - -
   * - automount
     - boolean
     - Auto mount volume after attach.
     - `True`

Detach Volume to a Server
-------------------------------

.. code-block:: python

  #client = HcloudClient(token="Your-Project-Token")
  #volume = client.volumes.get_by_id(123)
   volume.detach()

**Return:** :ref:`action_domain`

`API Documentation <https://docs.hetzner.cloud/#volume-actions-detach-volume>`_

Detach Volume to a Server
-------------------------------

.. code-block:: python

  #client = HcloudClient(token="Your-Project-Token")
  #volume = client.volumes.get_by_id(123)
   volume.resize(size=50)

**Return:** :ref:`action_domain`

`API Documentation <https://docs.hetzner.cloud/#volume-actions-resize-volume>`_

.. list-table::
   :widths: 15 10 10 30
   :header-rows: 1

   * - Parameter
     - Type
     - Description
     - Sample
   * - size
     - int
     - New volume size in GB (must be greater than current size)
     - -

Change protection for a Volume
-------------------------------

.. code-block:: python

  #client = HcloudClient(token="Your-Project-Token")
  #volume = client.volumes.get_by_id(123)
   volume.change_protection(delete=True)

**Return:** :ref:`action_domain`

`API Documentation <https://docs.hetzner.cloud/#volume-actions-change-volume-protection>`_

.. list-table::
   :widths: 15 10 10 30
   :header-rows: 1

   * - Parameter
     - Type
     - Description
     - Sample
   * - delete
     - boolean
     - If `True`, prevents the Volume from being deleted
     - `True`
