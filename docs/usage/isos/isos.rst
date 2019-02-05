ISOs
======================


Get all ISOs
----------------

.. code-block:: python

  #client = HcloudClient(token="Your-Project-Token")
   client.isos.get_all()

**Response:** List[:ref:`iso_domain`]

.. list-table::
   :widths: 15 10 10 30
   :header-rows: 1

   * - Parameter
     - Type
     - Description
     - Sample
   * - name
     - string (optional)
     - Can be used to filter isos by their name.
     - `FreeBSD-11.0-RELEASE-amd64-dvd1`

List ISOs
-----------------

List ISOs with more granular control over how many ISOs will be returned.

.. code-block:: python

  #client = HcloudClient(token="Your-Project-Token")
   client.isos.get_list()

**Response:** List[:ref:`iso_domain`]

.. list-table::
   :widths: 15 10 10 30
   :header-rows: 1

   * - Parameter
     - Type
     - Description
     - Sample
   * - name
     - string (optional)
     - Can be used to filter isos by their name.
     - `FreeBSD-11.0-RELEASE-amd64-dvd1`
   * - page
     - string (optional)
     - Get all servers listed at a specific page.
     - `1`
   * - per_page
     - string (optional)
     - Specify the number of servers listed per page. Default: `25` Max: `50`
     - `25`
