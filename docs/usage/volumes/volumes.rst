Volumes
======================


Get all Volumes
----------------

.. code-block:: python

  #client = HcloudClient(token="Your-Project-Token")
   client.volumes.get_all()

**Return:** List[:ref:`volume_domain`]

`API Documentation <https://docs.hetzner.cloud/#volumes-get-all-volumes>`_

.. list-table::
   :widths: 15 10 10 30
   :header-rows: 1

   * - Parameter
     - Type
     - Description
     - Sample
   * - label_selector
     - str (optional)
     - Can be used to filter Volumes by labels. The response will only contain Volumes matching the label selector. For more details head over to: `Hetzner Cloud API Documentation <https://docs.hetzner.cloud/#overview-label-selector>`_.
     - `k==v`

List all Volumes
-----------------

List all Volumes with more granular control over how many Volumes will be returned.

.. code-block:: python

  #client = HcloudClient(token="Your-Project-Token")
   client.volumes.get_list()

**Return:** List[:ref:`volume_domain`]

`API Documentation <https://docs.hetzner.cloud/#volumes-get-all-volumes>`_

.. list-table::
   :widths: 15 10 10 30
   :header-rows: 1

   * - Parameter
     - Type
     - Description
     - Sample
   * - label_selector
     - string (optional)
     - Can be used to filter Volumes by labels. The response will only contain Volumes matching the label selector. For more details head over to: `Hetzner Cloud API Documentation <https://docs.hetzner.cloud/#overview-label-selector>`_.
     - `k==v`
   * - page
     - string (optional)
     - Get all Volumes listed at a specific page.
     - `1`
   * - per_page
     - string (optional)
     - Specify the number of Volumes listed per page. Default: `25` Max: `50`
     - `25`

Get a specific Volume
---------------------

.. code-block:: python

  #client = HcloudClient(token="Your-Project-Token")
   client.volumes.get_by_id(1234)

**Return:** :ref:`volume_domain`

`API Documentation <https://docs.hetzner.cloud/#volumes-get-an-volume>`_

Create a Volume
---------------------

.. code-block:: python

  #client = HcloudClient(token="Your-Project-Token")
   client.volumes.create(name="test-database", size=42, location=Location(name="nbg1"))

**Return:** :ref:`volume_domain`

`API Documentation <https://docs.hetzner.cloud/#volumes-create-a-volume>`_

.. list-table::
   :widths: 15 10 10 30
   :header-rows: 1

   * - Parameter
     - Type
     - Description
     - Sample
   * - name
     - str
     - Name of the volume
     - `my-volume`
   * - size
     - int
     - Size of the volume in GB
     - `42`
   * - labels
     - List[:ref:`labels_domain`] (optional)
     - New labels
     - -
   * - automount
     - boolean (optional)
     - Auto mount volume after attach. `server` must be provided.
     - `True`
   * - format
     - str (optional)
     - Format volume after creation. One of: `xfs`, `ext4`
     - `ext4`
   * - location
     - :ref:`location_domain` (optional)
     - Location to create the volume in (can be omitted if server is specified)
     - -
   * - server
     - :ref:`server_domain` (optional)
     - Server to which to attach the volume once it’s created (volume will be created in the same location as the server)
     - -

Update a Volume
-----------------
.. code-block:: python

  #client = HcloudClient(token="Your-Project-Token")
  #volume = client.volumes.get_by_id(123)
   volume.update(name="new-name")

**Return:** :ref:`volume_domain`

`API Documentation <https://docs.hetzner.cloud/#volumes-update-an-volume>`_

.. list-table::
   :widths: 15 10 10 30
   :header-rows: 1

   * - Parameter
     - Type
     - Description
     - Sample
   * - name
     - string (optional)
     - New name to set
     - `new-name`
   * - labels
     - List[:ref:`labels_domain`] (optional)
     - New labels
     - -

Delete a Volume
-----------------

.. code-block:: python

  #client = HcloudClient(token="Your-Project-Token")
  #volume = client.volumes.get_by_id(123)
   volume.delete()

**Return:** `boolean`

`API Documentation <https://docs.hetzner.cloud/#volumes-delete-an-volume>`_
