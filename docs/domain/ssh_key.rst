.. _ssh_key_domain:

SSH Key Domain
**************

.. code-block:: python

    from hcloud.ssh_keys.client import BoundSSHKey


.. list-table:: Properties
   :widths: 15 15 10 10
   :header-rows: 1

   * - Property
     - Type
     - Description
     - Sample
   * - id
     - int
     - ID of the SSH key
     - `123`
   * - name
     - str
     - Name of the SSH key (must be unique per project)
     - `My ssh key`
   * - fingerprint
     - str
     - Fingerprint of public key
     - `b7:2f:30:a0:2f:6c:58:6c:21:04:58:61:ba:06:3b:2f`
   * - public_key
     - str
     - Public key
     - `ssh-rsa AAAjjk76kgf...Xt`
   * - labels
     - List[:ref:`labels_domain`]
     - User-defined labels (key-value pairs)
     - -

You can find more information about this resource in our `API Documentation <https://docs.hetzner.cloud/#ssh-keys>`_.