Floating IP Actions
======================

List Actions
------------------

List Actions from the Image with more granular control over how many Actions will be returned.

.. code-block:: python

  #client = HcloudClient(token="Your-Project-Token")
  #floating_ip = client.floating_ips.get_by_id(123)
  floating_ip.get_actions_list(status=["running"],sort=["id","progress:desc"])

**Return:** List[:ref:`action_domain`]

`API Documentation <https://docs.hetzner.cloud/#floating-ip-actions-get-all-actions-for-a-floating-ip>`_

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
  #floating_ip = client.floating_ips.get_by_id(123)
   floating_ip.get_actions(status=["running"],sort=["id","progress:desc"])

**Return:** List[:ref:`action_domain`]

`API Documentation <https://docs.hetzner.cloud/#floating-ip-actions-get-all-actions-for-a-floating-ip>`_

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

Assign a Floating IP
-------------------------------

.. code-block:: python

  #client = HcloudClient(token="Your-Project-Token")
  #floating_ip = client.floating_ips.get_by_id(123)
   floating_ip.assign(server=Server(id=123))

**Return:** :ref:`action_domain`

`API Documentation <https://docs.hetzner.cloud/#floating-ip-actions-assign-a-floating-ip-to-a-server>`_

.. list-table::
   :widths: 15 10 10 30
   :header-rows: 1

   * - Parameter
     - Type
     - Description
     - Sample
   * - server
     - :ref:`server_domain`
     - Server the Floating IP shall be assigned to
     - -


Unassign a Floating IP
-------------------------------

.. code-block:: python

  #client = HcloudClient(token="Your-Project-Token")
  #floating_ip = client.floating_ips.get_by_id(123)
   floating_ip.unassign()

**Return:** :ref:`action_domain`

`API Documentation <https://docs.hetzner.cloud/#floating-ip-actions-unassign-a-floating-ip>`_

Change reverse DNS entry for a Floating IP
-------------------------------------------

.. code-block:: python

  #client = HcloudClient(token="Your-Project-Token")
  #floating_ip = client.floating_ips.get_by_id(123)
   floating_ip.change_dns_ptr(ip="1.2.3.4", dns_ptr="server01.example.com")

**Return:** :ref:`action_domain`

`API Documentation <https://docs.hetzner.cloud/#floating-ip-actions-change-reverse-dns-entry-for-this-server>`_

.. list-table::
   :widths: 15 10 10 30
   :header-rows: 1

   * - Parameter
     - Type
     - Description
     - Sample
   * - ip
     - str
     - IP address for which to set the reverse DNS entry
     - `1.2.3.4`
   * - dns_ptr
     - str, `None`
     - Hostname to set as a reverse DNS PTR entry, will reset to original default value if `None`
     - `server01.example.com`

Change protection for a Floating IP
------------------------------------

.. code-block:: python

  #client = HcloudClient(token="Your-Project-Token")
  #floating_ip = client.floating_ips.get_by_id(123)
   floating_ip.change_protection(delete=True)

**Return:** :ref:`action_domain`

`API Documentation <https://docs.hetzner.cloud/#image-actions-get-all-actions-for-an-image>`_

.. list-table::
   :widths: 15 10 10 30
   :header-rows: 1

   * - Parameter
     - Type
     - Description
     - Sample
   * - delete
     - boolean
     - If `True`, prevents the Floating IP from being deleted
     - `True`
