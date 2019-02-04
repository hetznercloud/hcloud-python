.. _action_domain:

Action Domain
**************

.. code-block:: python

    from hcloud.actions.client import BoundAction


.. list-table:: Properties
   :widths: 15 15 10 10
   :header-rows: 1

   * - Property
     - Type
     - Description
     - Sample
   * - id
     - int
     - ID of the action
     - `123`
   * - command
     - str
     - Command executed in the action
     - `start_server`
   * - status
     - str
     - Status of the action
     - `running`
   * - progress
     - int
     - Progress of action in percent
     - `100`
   * - started
     - str
     - Point in time when the action was started (in ISO-8601 format)
     - `2016-01-30T23:50+00:00`
   * - finished
     - str, null
     - Point in time when the action was finished (in ISO-8601 format). Only set if the action is finished otherwise null.
     - `2016-01-30T23:50+00:00`
   * - resources
     - tuple
     - Resources the action relates to
     - -
   * - error
     - tuple, null
     - Error message for the action if error occured, otherwise null.
     - -