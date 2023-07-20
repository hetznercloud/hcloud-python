API References
==================

Main Interface
---------------

.. autoclass:: hcloud.Client
    :members:


API Clients
-------------
.. toctree::
   :maxdepth: 3
   :glob:

   api.clients.*

Exceptions
---------------

.. autoclass:: hcloud.HCloudException
    :members:

.. autoclass:: hcloud.APIException
    :members:

.. autoclass:: hcloud.actions.domain.ActionException
    :members:

.. autoclass:: hcloud.actions.domain.ActionFailedException
    :members:

.. autoclass:: hcloud.actions.domain.ActionTimeoutException
    :members:

Other
-------------

.. toctree::
   :maxdepth: 3

   api.helpers
   api.deprecation
