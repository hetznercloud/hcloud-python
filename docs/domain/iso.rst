.. _iso_domain:

ISO Domain
**************

.. code-block:: python

    from hcloud.isos.client import BoundIso


.. list-table:: Properties
   :widths: 15 15 10 10
   :header-rows: 1

   * - Property
     - Type
     - Description
     - Sample
   * - id
     - int
     - ID of the ISO
     - `123`
   * - name
     - str
     - Unique identifier of the ISO. Only set for public ISOs
     - `FreeBSD-11.0-RELEASE-amd64-dvd1`
   * - description
     - str
     - Description of the iso
     - `FreeBSD 11.0 x64`
   * - type
     - str
     - Type of the ISO
     - `public`
   * - deprecated
     - string, null
     - ISO 8601 timestamp of deprecation, null if ISO is still available.
     - `2016-01-30T23:50+00:00`

