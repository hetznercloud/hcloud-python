from __future__ import annotations

import warnings
from typing import TYPE_CHECKING, TypedDict

from ..core import BaseDomain, DomainIdentityMixin

if TYPE_CHECKING:
    from ..actions import BoundAction
    from ..datacenters import BoundDatacenter
    from ..locations import BoundLocation
    from ..rdns import DNSPtr
    from .client import BoundPrimaryIP

__all__ = [
    "PrimaryIP",
    "PrimaryIPProtection",
    "CreatePrimaryIPResponse",
]


class PrimaryIP(BaseDomain, DomainIdentityMixin):
    """Primary IP Domain

    :param id: int
           ID of the Primary IP
    :param ip: str
           IP address of the Primary IP
    :param type: str
           Type of Primary IP. Choices: `ipv4`, `ipv6`
    :param dns_ptr: List[Dict]
           Array of reverse DNS entries
    :param datacenter: :class:`Datacenter <hcloud.datacenters.client.BoundDatacenter>`
        Datacenter the Primary IP was created in.

        This property is deprecated and will be removed after 1 July 2026.
        Please use the ``location`` property instead.

        See https://docs.hetzner.cloud/changelog#2025-12-16-phasing-out-datacenters.

    :param location: :class:`Location <hcloud.locations.client.BoundLocation>`
           Location the Primary IP was created in.
    :param blocked: boolean
           Whether the IP is blocked
    :param protection: dict
           Protection configuration for the Primary IP
    :param labels: dict
           User-defined labels (key-value pairs)
    :param created: datetime
           Point in time when the Primary IP was created
    :param name: str
           Name of the Primary IP
    :param assignee_id: int
           Assignee ID the Primary IP is assigned to
    :param assignee_type: str
           Assignee Type of entity the Primary IP is assigned to
    :param auto_delete: bool
           Delete the Primary IP when the Assignee it is assigned to is deleted.
    """

    __properties__ = (
        "id",
        "ip",
        "type",
        "dns_ptr",
        "location",
        "blocked",
        "protection",
        "labels",
        "created",
        "name",
        "assignee_id",
        "assignee_type",
        "auto_delete",
    )
    __api_properties__ = (
        *__properties__,
        "datacenter",
    )
    __slots__ = (
        *__properties__,
        "_datacenter",
    )

    def __init__(
        self,
        id: int | None = None,
        type: str | None = None,
        ip: str | None = None,
        dns_ptr: list[DNSPtr] | None = None,
        datacenter: BoundDatacenter | None = None,
        location: BoundLocation | None = None,
        blocked: bool | None = None,
        protection: PrimaryIPProtection | None = None,
        labels: dict[str, str] | None = None,
        created: str | None = None,
        name: str | None = None,
        assignee_id: int | None = None,
        assignee_type: str | None = None,
        auto_delete: bool | None = None,
    ):
        self.id = id
        self.type = type
        self.ip = ip
        self.dns_ptr = dns_ptr
        self.datacenter = datacenter
        self.location = location
        self.blocked = blocked
        self.protection = protection
        self.labels = labels
        self.created = self._parse_datetime(created)
        self.name = name
        self.assignee_id = assignee_id
        self.assignee_type = assignee_type
        self.auto_delete = auto_delete

    @property
    def datacenter(self) -> BoundDatacenter | None:
        """
        :meta private:
        """
        warnings.warn(
            "The 'datacenter' property is deprecated and will be removed after 1 July 2026. "
            "Please use the 'location' property instead. "
            "See https://docs.hetzner.cloud/changelog#2025-12-16-phasing-out-datacenters.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self._datacenter

    @datacenter.setter
    def datacenter(self, value: BoundDatacenter | None) -> None:
        self._datacenter = value


class PrimaryIPProtection(TypedDict):
    delete: bool


class CreatePrimaryIPResponse(BaseDomain):
    """Create Primary IP Response Domain

    :param primary_ip: :class:`BoundPrimaryIP <hcloud.primary_ips.client.BoundPrimaryIP>`
           The Primary IP which was created
    :param action: :class:`BoundAction <hcloud.actions.client.BoundAction>`
           The Action which shows the progress of the Primary IP Creation
    """

    __api_properties__ = ("primary_ip", "action")
    __slots__ = __api_properties__

    def __init__(
        self,
        primary_ip: BoundPrimaryIP,
        action: BoundAction | None,
    ):
        self.primary_ip = primary_ip
        self.action = action
