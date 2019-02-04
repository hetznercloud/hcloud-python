.. _location_domain:

Location Domain
****************

.. code-block:: python

    from hcloud.locations.client import BoundLocation


.. list-table:: Properties
   :widths: 15 15 10 10
   :header-rows: 1

   * - Property
     - Type
     - Description
     - Sample
   * - id
     - int
     - ID of the location
     - `123`
   * - name
     - str
     - Unique identifier of the location
     - `fsn1`
   * - description
     - str
     - Description of the location
     - `Falkenstein DC Park 1`
   * - country
     - str
     - ISO 3166-1 alpha-2 code of the country the location resides in
     - `DE`
   * - city
     - str
     - City the location is closest to
     - Falkenstein
   * - latitude
     - float
     - Latitude of the city closest to the location
     - 50.47612
   * - longitude
     - float
     - Longitude of the city closest to the location
     - 12.370071