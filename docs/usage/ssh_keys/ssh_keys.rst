SSH-Keys
======================


Get all ssh keys
----------------

Get all SSH keys from within the account of the API token.

.. code-block:: python

  #client = HcloudClient(token="Your-Project-Token")
   client.ssh_keys.get_all()

**Response:** List[:ref:`ssh_key_domain`]

.. list-table::
   :widths: 15 10 10 30
   :header-rows: 1

   * - Parameter
     - Type
     - Description
     - Sample
   * - name
     - string (optional)
     - Can be used to filter ssh keys by their name. The response will only contain the ssh key matching the specified name.
     - `my-ssh-key`
   * - fingerprint
     - string (optional)
     - Can be used to filter SSH keys by their fingerprint. The response will only contain the SSH key matching the specified fingerprint.
     - `b7:2f:30:a0:2f:6c:58:6c:21:04:58:61:ba:06:3b:2f`
   * - label_selector
     - string (optional)
     - Can be used to filter ssh keys by labels. The response will only contain ssh keys matching the label selector. For more details head over to: `Hetzner Cloud API Documentation <https://docs.hetzner.cloud/#overview-label-selector>`_.
     - `k==v`

List all ssh keys
-----------------

List all ssh keys with more granular control over how many ssh keys will be returned.

.. code-block:: python

  #client = HcloudClient(token="Your-Project-Token")
   client.ssh_keys.get_list()

**Response:** List[:ref:`ssh_key_domain`]

.. list-table::
   :widths: 15 10 10 30
   :header-rows: 1

   * - Parameter
     - Type
     - Description
     - Sample
   * - name
     - string (optional)
     - Can be used to filter ssh keys by their name. The response will only contain the ssh key matching the specified name.
     - `my-ssh_key`
   * - fingerprint
     - string (optional)
     - Can be used to filter SSH keys by their fingerprint. The response will only contain the SSH key matching the specified fingerprint.
     - `b7:2f:30:a0:2f:6c:58:6c:21:04:58:61:ba:06:3b:2f`
   * - label_selector
     - string (optional)
     - Can be used to filter ssh keys by labels. The response will only contain ssh keys matching the label selector. For more details head over to: `Hetzner Cloud API Documentation <https://docs.hetzner.cloud/#overview-label-selector>`_.
     - `k==v`
   * - page
     - string (optional)
     - Get all ssh keys listed at a specific page.
     - `1`
   * - per_page
     - string (optional)
     - Specify the number of ssh keys listed per page. Default: `25` Max: `50`
     - `25`

Get a specific ssh key
-----------------

Returns a specific ssh key object. The ssh key must exist inside the project.

.. code-block:: python

  #client = HcloudClient(token="Your-Project-Token")
   client.ssh_keys.get_by_id(1234)

**Response:** :ref:`ssh_key_domain`


Create a ssh key
-----------------

Creates a new ssh key. Returns preliminary information about the ssh key as well as an action that covers progress of creation.

.. code-block:: python

  #client = HcloudClient(token="Your-Project-Token")
   client.ssh_keys.create(name="my-ssh key", public_key="ssh-rsa AAAjjk76kgf...Xt")

**Response:** :ref:`ssh_key_domain`


.. list-table::
   :widths: 15 10 10 30
   :header-rows: 1

   * - Parameter
     - Type
     - Description
     - Sample
   * - name
     - string
     - Name of the ssh key
     - `my-ssh key`
   * - public_key
     - str
     - Public key
     - `ssh-rsa AAAjjk76kgf...Xt`


Update a ssh key
-----------------

Updates a ssh key.

.. code-block:: python

  #client = HcloudClient(token="Your-Project-Token")
  #ssh_key = client.ssh_key.get_by_id(123)
   ssh_key.update(name="new-name")

**Response:** :ref:`ssh_key_domain`


.. list-table::
   :widths: 15 10 10 30
   :header-rows: 1

   * - Parameter
     - Type
     - Description
     - Sample
   * - name
     - string
     - New name to set
     - `new-name`
   * - labels
     - List[:ref:`labels_domain`] (optional)
     - New labels
     - -

Delete a ssh key
-----------------

Deletes an SSH key. It cannot be used anymore.

.. code-block:: python

  #client = HcloudClient(token="Your-Project-Token")
  #ssh_key = client.ssh_key.get_by_id(123)
   ssh_key.delete()

**Response:** `boolean`