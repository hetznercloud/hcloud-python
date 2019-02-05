.. _labels_domain:

Labels Domain
**************

Labels are Key Value pairs.

.. code-block:: python

    label = {"key":"value"} # One Label
    labels = [{"key":"value"},{"another_key":"value"}] # Many Labels

See our `API Documentation <https://docs.hetzner.cloud/#overview-labels>`_ for more details about the Labels.

.. _protection_domain:

Protection Domain
**************

Servers, snapshots and Floating IPs can now be protected from accidental deletion and rebuild via the protection configuration.

.. code-block:: python

    protection = {
      "delete": False,
      "rebuild": False, # Only on servers
    }
