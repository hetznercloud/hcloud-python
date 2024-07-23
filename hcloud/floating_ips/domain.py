from __future__ import annotations

from typing import TYPE_CHECKING

from dateutil.parser import isoparse

from ..core import BaseDomain, DomainIdentityMixin

if TYPE_CHECKING:
    from ..actions import BoundAction
    from ..locations import BoundLocation
    from ..servers import BoundServer
    from .client import BoundFloatingIP


class FloatingIP(BaseDomain, DomainIdentityMixin):
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

    __api_properties__ = (
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
    __slots__ = __api_properties__

    def __init__(
        self,
        id: int | None = None,
        type: str | None = None,
        description: str | None = None,
        ip: str | None = None,
        server: BoundServer | None = None,
        dns_ptr: list[dict] | None = None,
        home_location: BoundLocation | None = None,
        blocked: bool | None = None,
        protection: dict | None = None,
        labels: dict[str, str] | None = None,
        created: str | None = None,
        name: str | None = None,
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

    __api_properties__ = ("floating_ip", "action")
    __slots__ = __api_properties__

    def __init__(
        self,
        floating_ip: BoundFloatingIP,
        action: BoundAction | None,
    ):
        self.floating_ip = floating_ip
        self.action = action
