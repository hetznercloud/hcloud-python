Actions
======================


Get all Actions
----------------

.. code-block:: python

  #client = HcloudClient(token="Your-Project-Token")
   client.actions.get_all()

**Return:** List[:ref:`action_domain`]

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

List Actions
-----------------

List Actions with more granular control over how many Actions will be returned.

.. code-block:: python

  #client = HcloudClient(token="Your-Project-Token")
   client.actions.get_list()

**Return:** List[:ref:`action_domain`]

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
     - Get all servers listed at a specific page.
     - `1`
   * - per_page
     - string (optional)
     - Specify the number of servers listed per page. Default: `25` Max: `50`
     - `25`

Get a specific Action
-----------------------

Returns a specific Action object.

.. code-block:: python

  #client = HcloudClient(token="Your-Project-Token")
   client.actions.get_by_id(1234)

**Return:** :ref:`action_domain`