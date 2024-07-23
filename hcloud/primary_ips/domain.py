from __future__ import annotations

from typing import TYPE_CHECKING

from dateutil.parser import isoparse

from ..core import BaseDomain, DomainIdentityMixin

if TYPE_CHECKING:
    from ..actions import BoundAction
    from ..datacenters import BoundDatacenter
    from .client import BoundPrimaryIP


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

    __api_properties__ = (
        "id",
        "ip",
        "type",
        "dns_ptr",
        "datacenter",
        "blocked",
        "protection",
        "labels",
        "created",
        "name",
        "assignee_id",
        "assignee_type",
        "auto_delete",
    )
    __slots__ = __api_properties__

    def __init__(
        self,
        id: int | None = None,
        type: str | None = None,
        ip: str | None = None,
        dns_ptr: list[dict] | None = None,
        datacenter: BoundDatacenter | None = None,
        blocked: bool | None = None,
        protection: dict | None = None,
        labels: dict[str, dict] | None = None,
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
        self.blocked = blocked
        self.protection = protection
        self.labels = labels
        self.created = isoparse(created) if created else None
        self.name = name
        self.assignee_id = assignee_id
        self.assignee_type = assignee_type
        self.auto_delete = auto_delete


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
