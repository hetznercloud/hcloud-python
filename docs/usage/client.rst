Client
*******

Basic Configuration
^^^^^^^^^^^^^^^^^^^^^^^

Create a reusable basic hcloud-python client.

.. code-block:: python

   from hcloud import HcloudClient
   client = HcloudClient(token="Your-Project-Token")


Advanced Configuration
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from hcloud import HcloudClient
   client = HcloudClient(token="Your-Project-Token")


.. list-table:: Parameters
   :widths: 15 10 30
   :header-rows: 1

   * - Parameter
     - Description
     - Sample
   * - token
     - (required) Hetzner Cloud API Token
     - `jmvQpvMeEQsTtdpFhzMnkqCafNSUqMKqufFgrQcsxcJuQmxLmQacHGuXAyyRMYhT`