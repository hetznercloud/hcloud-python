Locations
======================


Get all locations
----------------

Get all locations.

.. code-block:: python

  #client = HcloudClient(token="Your-Project-Token")
   client.locations.get_all()

**Response:** List[:ref:`location_domain`]

.. list-table::
   :widths: 15 10 10 30
   :header-rows: 1

   * - Parameter
     - Type
     - Description
     - Sample
   * - name
     - string (optional)
     - Can be used to filter locations by their name.
     - `fsn1`

List locations
-----------------

List locations with more granular control over how many locations will be returned.

.. code-block:: python

  #client = HcloudClient(token="Your-Project-Token")
   client.locations.get_list()

**Response:** List[:ref:`location_domain`]

.. list-table::
   :widths: 15 10 10 30
   :header-rows: 1

   * - Parameter
     - Type
     - Description
     - Sample
   * - name
     - string (optional)
     - Can be used to filter locations by their name.
     - `fsn1`
   * - page
     - string (optional)
     - Get all servers listed at a specific page.
     - `1`
   * - per_page
     - string (optional)
     - Specify the number of servers listed per page. Default: `25` Max: `50`
     - `25`
