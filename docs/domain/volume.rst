.. _volume_domain:

Volume Domain
**************

.. code-block:: python

    from hcloud.volumes.client import BoundVolume


.. list-table:: Properties
   :widths: 15 15 10 10
   :header-rows: 1

   * - Property
     - Type
     - Description
     - Sample
   * - id
     - int
     - ID of the Volume
     - `4711`
   * - created
     - str
     - Timestamp when volume was created
     - `2016-01-30T23:50+00:00`
   * - name
     - str
     - Name of the Volume
     - database-storage`
   * - server
     - ref:`server_domain`, `None`
     - Server the Volume is attached to, `None` if it is not attached at all.
     - -
   * - location
     - ref:`location_domain`
     - Location of the Volume. Volume can only be attached to Servers in the same location.
     - -
   * - size
     - int
     - Size in GB of the Volume
     - `42`
   * - linux_device
     - str
     - Device path on the file system for the Volume
     - `/dev/disk/by-id/scsi-0HC_Volume_4711`
   * - protection
     - List[:ref:`protection_domain`]
     - Protection configuration for the Floating IP
     - -
   * - labels
     - List[:ref:`labels_domain`]
     - User-defined labels (key-value pairs)
     - -
   * - status
     - str
     - Current status of the volume
     - `available`