Floating IPs
======================


Get all Floating IPs
---------------------

.. code-block:: python

  #client = HcloudClient(token="Your-Project-Token")
   client.floating_ips.get_all()

**Return:** List[:ref:`floating_ip_domain`]

`API Documentation <https://docs.hetzner.cloud/#floating-ips-get-all-floating-ips>`_

.. list-table::
   :widths: 15 10 10 30
   :header-rows: 1

   * - Parameter
     - Type
     - Description
     - Sample
   * - label_selector
     - string (optional)
     - Can be used to filter Floating IPs by labels. The response will only contain Floating IPs matching the label selector. For more details head over to: `Hetzner Cloud API Documentation <https://docs.hetzner.cloud/#overview-label-selector>`_.
     - `k==v`

List all Floating IPs
----------------------

List all Floating IPs with more granular control over how many Floating IPs will be returned.

.. code-block:: python

  #client = HcloudClient(token="Your-Project-Token")
   client.floating_ips.get_list()

**Return:** List[:ref:`floating_ip_domain`]

`API Documentation <https://docs.hetzner.cloud/#floating-ips-get-all-floating-ips>`_

.. list-table::
   :widths: 15 10 10 30
   :header-rows: 1

   * - Parameter
     - Type
     - Description
     - Sample
   * - label_selector
     - string (optional)
     - Can be used to filter Floating IPs by labels. The response will only contain Floating IPs matching the label selector. For more details head over to: `Hetzner Cloud API Documentation <https://docs.hetzner.cloud/#overview-label-selector>`_.
     - `k==v`
   * - page
     - string (optional)
     - Get all Floating IPs listed at a specific page.
     - `1`
   * - per_page
     - string (optional)
     - Specify the number of Floating IPs listed per page. Default: `25` Max: `50`
     - `25`

Get a specific Floating IP
---------------------------

.. code-block:: python

  #client = HcloudClient(token="Your-Project-Token")
   client.floating_ips.get_by_id(1234)

**Return:** :ref:`floating_ip_domain`

`API Documentation <https://docs.hetzner.cloud/#floating-ips-get-a-specific-floating-ip>`_

Create a Floating IP
---------------------

.. code-block:: python

  #client = HcloudClient(token="Your-Project-Token")
   client.floating_ips.create(type="ipv4", home_location=Location(name="fsn1"))

**Return:** :ref:`floating_ip_domain`

`API Documentation <https://docs.hetzner.cloud/#floating-ips-create-a-floating-ip>`_

.. list-table::
   :widths: 15 10 10 30
   :header-rows: 1

   * - Parameter
     - Type
     - Description
     - Sample
   * - description
     - string (optional)
     - Description of the Floating IP
     - `my-Floating IP`
   * - server
     - :ref:`server_domain` (optinal)
     - Server the Floating IP is assigned to
     - -
   * - home_location
     - :ref:`location_domain`
     - Home location (routing is optimized for that location).
     - -
   * - labels
     - List[:ref:`labels_domain`] (optional)
     - User-defined labels (key-value pairs)
     - -

Update a Floating IP
---------------------

.. code-block:: python

  #client = HcloudClient(token="Your-Project-Token")
  #floating_ip = client.floating_ips.get_by_id(123)
   floating_ip.update(description="new-description")

**Return:** :ref:`floating_ip_domain`

`API Documentation <https://docs.hetzner.cloud/#floating-ips-update-a-floating-ip>`_

.. list-table::
   :widths: 15 10 10 30
   :header-rows: 1

   * - Parameter
     - Type
     - Description
     - Sample
   * - description
     - string
     - New description to set
     - `new-description`
   * - labels
     - List[:ref:`labels_domain`] (optional)
     - New labels
     - -

Delete a Floating IP
---------------------

.. code-block:: python

  #client = HcloudClient(token="Your-Project-Token")
  #floating_ip = client.floating_ips.get_by_id(123)
   floating_ip.delete()

**Return:** `boolean`

`API Documentation <https://docs.hetzner.cloud/#floating-ips-delete-a-floating-ip>`_
