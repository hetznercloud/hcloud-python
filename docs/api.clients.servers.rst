ServersClient
==================


Waiting for a graceful shutdown
-------------------------------

The shutdown action sends an ACPI request to the guest operating system.
:meth:`~hcloud.actions.client.BoundAction.wait_until_finished` waits for that
request to be sent, rather than for the guest to stop. Before changing the
server type or performing another operation that requires a stopped server,
reload its status until it is :attr:`~hcloud.servers.domain.Server.STATUS_OFF`.

For an existing :class:`~hcloud.servers.client.BoundServer` named ``server``,
the following example checks the status at most 60 times. It raises a timeout
instead of continuing if the guest does not shut down::

    from time import sleep

    from hcloud.servers.domain import Server

    server.shutdown().wait_until_finished()
    for attempt in range(60):
        server.reload()
        if server.status == Server.STATUS_OFF:
            break
        if attempt < 59:
            sleep(1)
    else:
        raise TimeoutError("Server did not shut down after 60 status checks")

A guest may ignore the request, for example if it does not handle ACPI.
Choose the polling interval and limit to suit the workload. A forced
:meth:`~hcloud.servers.client.BoundServer.power_off` cuts power without a clean
guest shutdown; this example does not fall back to it automatically.

.. autoclass:: hcloud.servers.client.ServersClient
    :members:

.. autoclass:: hcloud.servers.client.BoundServer
    :members:

.. autoclass:: hcloud.servers.domain.Server
    :members:

.. autoclass:: hcloud.servers.domain.PublicNetwork
    :members:

.. autoclass:: hcloud.servers.domain.IPv4Address
    :members:

.. autoclass:: hcloud.servers.domain.IPv6Network
    :members:

.. autoclass:: hcloud.servers.domain.CreateServerResponse
    :members:

.. autoclass:: hcloud.servers.domain.ServerCreatePublicNetwork
    :members:

.. autoclass:: hcloud.servers.domain.ResetPasswordResponse
    :members:

.. autoclass:: hcloud.servers.domain.EnableRescueResponse
    :members:

.. autoclass:: hcloud.servers.domain.RequestConsoleResponse
    :members:
