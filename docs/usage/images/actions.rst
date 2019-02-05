Image Actions
======================

List Actions
------------------

Returns a list of action domains for an Image.

.. code-block:: python

  #client = HcloudClient(token="Your-Project-Token")
  #image = client.images.get_by_id(123)
   image.get_actions_list(status=["running"],sort=["id","progress:desc"])

**Return:** List[:ref:`action_domain`]

`API Documentation <https://docs.hetzner.cloud/#image-actions-get-all-actions-for-an-image>`_

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

Returns all action objects for an Image.

.. code-block:: python

  #client = HcloudClient(token="Your-Project-Token")
  #image = client.images.get_by_id(123)
   image.get_actions(status=["running"],sort=["id","progress:desc"])

**Return:** List[:ref:`action_domain`]

`API Documentation <https://docs.hetzner.cloud/#image-actions-get-all-actions-for-an-image>`_

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

Change protection for an Image
-------------------------------

Changes the protection configuration of the Image.

.. code-block:: python

  #client = HcloudClient(token="Your-Project-Token")
  #image = client.images.get_by_id(123)
   image.change_protection(delete=True)

**Return:** :ref:`action_domain`

`API Documentation <https://docs.hetzner.cloud/#image-actions-change-protection-for-an-image>`_

.. list-table::
   :widths: 15 10 10 30
   :header-rows: 1

   * - Parameter
     - Type
     - Description
     - Sample
   * - delete
     - boolean
     - If true, prevents the Image from being deleted
     - `True`
