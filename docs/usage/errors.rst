Error Handling
*******

On every request that was not successfully a `HcloudAPIException` will be raised.

A `HcloudAPIException` contains the `code`, the `message` and some `details`.

You can find an overview over all errors on our `API Documentation <https://docs.hetzner.cloud/#overview-errors>`_.