.. _image_domain:

Image Domain
**************

.. code-block:: python

    from hcloud.images.client import BoundImage


.. list-table:: Properties
   :widths: 15 15 10 10
   :header-rows: 1

   * - Property
     - Type
     - Description
     - Sample
   * - id
     - int
     - ID of the image
     - `123`
   * - type
     - str
     - Type of the image
     - `system`
   * - status
     - str
     - Whether the image can be used or if it’s still being created
     - `running`
   * - name
     - str, null
     - Unique identifier of the image. This value is only set for system images.
     - `ubuntu-16.04`
   * - description
     - str
     - Description of the image
     - `Ubuntu 16.04 Standard 64 bit`
   * - image_size
     - float, null
     - Size of the image file in our storage in GB
     - `2.3`
   * - disk_size
     - float
     - Size of the disk contained in the image in GB.
     - `10`
   * - created
     - string
     - Point in time when the image was created (in ISO-8601 format)
     - `2016-01-30T23:50+00:00`
   * - created_from
     - :ref:`server_domain`, null
     - Information about the server the image was created from
     - -
   * - bound_to
     - :ref:`server_domain`, null
     - ID of server the image is bound to
     - -
   * - os_flavor
     - str
     - Flavor of operating system contained in the image
     - `ubuntu`
   * - os_flavor
     - str, null
     - Operating system version
     - `16.04`
   * - rapid_deploy
     - boolean
     - Indicates that rapid deploy of the image is available
     - `true`
   * - deprecated
     - string, null
     - Point in time when the image is considered to be deprecated (in ISO-8601 format)
     - `2016-01-30T23:50+00:00`
   * - protection
     - tuple
     - Protection configuration for the image
     - -
   * - labels
     - tuple
     - User-defined labels (key-value pairs)
     - -


.. _image_create_response_domain:

Create Image Response Domain
******************************

.. code-block:: python

    from hcloud.images.domain import CreateImageResponse


.. list-table:: Properties
   :widths: 15 15 10 10
   :header-rows: 1

   * - Property
     - Type
     - Description
     - Sample
   * - image
     - :ref:`image_domain`
     - Created image
     - -
   * - action
     - :ref:`action_domain`
     - Action that shows the progress of the image creation
     - -