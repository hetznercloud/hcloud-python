Images
======================


Get all Images
----------------

Returns all image objects.

.. code-block:: python

  #client = HcloudClient(token="Your-Project-Token")
   client.images.get_all()

**Return:** List[:ref:`image_domain`]

`API Documentation <https://docs.hetzner.cloud/#images-get-all-images>`_

.. list-table::
   :widths: 15 10 10 30
   :header-rows: 1

   * - Parameter
     - Type
     - Description
     - Sample
   * - label_selector
     - str (optional)
     - Can be used to filter Images by labels. The response will only contain Images matching the label selector. For more details head over to: `Hetzner Cloud API Documentation <https://docs.hetzner.cloud/#overview-label-selector>`_.
     - `k==v`
   * - type
     - List[str] (optional)
     - Type of Images
     - `["system","backup"]`
   * - bound_to
     - List[str] (optional)
     - Server Ids linked to the image. Only available for images of type `backup`
     - `[123,456]`
   * - name
     - str (optional)
     - Can be used to filter images by their name.
     - `ubuntu-16.04`

List all Images
-----------------

List all Images with more granular control over how many Images will be returned.

.. code-block:: python

  #client = HcloudClient(token="Your-Project-Token")
   client.images.get_list()

**Return:** List[:ref:`image_domain`]

`API Documentation <https://docs.hetzner.cloud/#images-get-all-images>`_

.. list-table::
   :widths: 15 10 10 30
   :header-rows: 1

   * - Parameter
     - Type
     - Description
     - Sample
   * - label_selector
     - string (optional)
     - Can be used to filter Images by labels. The response will only contain Images matching the label selector. For more details head over to: `Hetzner Cloud API Documentation <https://docs.hetzner.cloud/#overview-label-selector>`_.
     - `k==v`
   * - type
     - List[str] (optional)
     - Type of Images
     - `["system","backup"]`
   * - bound_to
     - List[str] (optional)
     - Server Ids linked to the image. Only available for images of type `backup`
     - `[123,456]`
   * - name
     - str (optional)
     - Can be used to filter images by their name.
     - `ubuntu-16.04`
   * - page
     - string (optional)
     - Get all Images listed at a specific page.
     - `1`
   * - per_page
     - string (optional)
     - Specify the number of Images listed per page. Default: `25` Max: `50`
     - `25`

Get a specific Image
---------------------

Returns a specific Image object. The Image must exist inside the project.

.. code-block:: python

  #client = HcloudClient(token="Your-Project-Token")
   client.images.get_by_id(1234)

**Return:** :ref:`image_domain`

`API Documentation <https://docs.hetzner.cloud/#images-get-an-image>`_

Update an Image
-----------------
.. code-block:: python

  #client = HcloudClient(token="Your-Project-Token")
  #image = client.images.get_by_id(123)
   image.update(description="new-description")

**Return:** :ref:`image_domain`

`API Documentation <https://docs.hetzner.cloud/#images-update-an-image>`_

.. list-table::
   :widths: 15 10 10 30
   :header-rows: 1

   * - Parameter
     - Type
     - Description
     - Sample
   * - description
     - string (optional)
     - New description to set
     - `new-description`
   * - type
     - string (optional)
     - New description to set
     - `snapshot`
   * - labels
     - List[:ref:`labels_domain`] (optional)
     - New labels
     - -

Delete an Image
-----------------

Deletes an Image. It cannot be used anymore.

.. code-block:: python

  #client = HcloudClient(token="Your-Project-Token")
  #image = client.images.get_by_id(123)
   image.delete()

**Return:** `boolean`

`API Documentation <https://docs.hetzner.cloud/#images-delete-an-image>`_
