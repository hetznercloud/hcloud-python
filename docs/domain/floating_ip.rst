.. _floating_ip_domain:

Floating IP Domain
**************

.. code-block:: python

    from hcloud.floating_ips.client import BoundFloatingIP


.. list-table:: Properties
   :widths: 15 15 10 10
   :header-rows: 1

   * - Property
     - Type
     - Description
     - Sample
   * - id
     - int
     - ID of the Floating IP
     - `123`
   * - description
     - str, `None`
     - Description of the Floating IP
     - `Web Frontend`
   * - ip
     - str
     - IP address of the Floating IP
     - `131.232.99.1`
   * - type
     - str
     - Type of the Floating IP
     - `ipv4`
   * - server
     - :ref:`server_domain`, `None`
     - Server the Floating IP is assigned to, `None` if it is not assigned at all.
     - -
   * - dns_ptr
     - List[tuple]
     - Array of reverse DNS entries
     - -
   * - home_location
     - :ref:`location_domain`
     - Location the Floating IP was created in.
     - -
   * - blocked
     - boolean
     - Whether the IP is blocked
     - `False`
   * - protection
     - List[:ref:`protection_domain`]
     - Protection configuration for the Floating IP
     - -
   * - labels
     - List[:ref:`labels_domain`]
     - User-defined labels (key-value pairs)
     - -