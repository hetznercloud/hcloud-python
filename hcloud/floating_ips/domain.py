# -*- coding: utf-8 -*-
from dateutil.parser import isoparse

from hcloud.core.domain import BaseDomain


class FloatingIP(BaseDomain):
    """Floating IP Domain

    :param id: int
           ID of the Floating IP
    :param description: str, None
           Description of the Floating IP
    :param ip: str
           IP address of the Floating IP
    :param type: str
           Type of Floating IP. Choices: `ipv4`, `ipv6`
    :param server: :class:`BoundServer <hcloud.servers.client.BoundServer>`, None
           Server the Floating IP is assigned to, None if it is not assigned at all
    :param dns_ptr: List[Dict]
           Array of reverse DNS entries
    :param home_location: :class:`BoundLocation <hcloud.locations.client.BoundLocation>`
           Location the Floating IP was created in. Routing is optimized for this location.
    :param blocked: boolean
           Whether the IP is blocked
    :param protection: dict
           Protection configuration for the Floating IP
    :param labels: dict
           User-defined labels (key-value pairs)
    :param created: datetime
           Point in time when the Floating IP was created
    :param name: str
           Name of the Floating IP
    """

    __slots__ = (
        "id",
        "type",
        "description",
        "ip",
        "server",
        "dns_ptr",
        "home_location",
        "blocked",
        "protection",
        "labels",
        "name",
        "created",
    )

    def __init__(
        self,
        id=None,
        type=None,
        description=None,
        ip=None,
        server=None,
        dns_ptr=None,
        home_location=None,
        blocked=None,
        protection=None,
        labels=None,
        created=None,
        name=None,
    ):
        self.id = id
        self.type = type
        self.description = description
        self.ip = ip
        self.server = server
        self.dns_ptr = dns_ptr
        self.home_location = home_location
        self.blocked = blocked
        self.protection = protection
        self.labels = labels
        self.created = isoparse(created) if created else None
        self.name = name


class CreateFloatingIPResponse(BaseDomain):
    """Create Floating IP Response Domain

    :param floating_ip: :class:`BoundFloatingIP <hcloud.floating_ips.client.BoundFloatingIP>`
           The Floating IP which was created
    :param action: :class:`BoundAction <hcloud.actions.client.BoundAction>`
           The Action which shows the progress of the Floating IP Creation
    """

    __slots__ = ("floating_ip", "action")

    def __init__(
        self,
        floating_ip,  # type: BoundFloatingIP
        action,  # type: BoundAction
    ):
        self.floating_ip = floating_ip
        self.action = action
