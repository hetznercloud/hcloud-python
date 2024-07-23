from __future__ import annotations

from typing import TYPE_CHECKING, Any

from dateutil.parser import isoparse

from ..core import BaseDomain, DomainIdentityMixin

if TYPE_CHECKING:
    from ..actions import BoundAction
    from ..servers import BoundServer, Server
    from .client import BoundFirewall


class Firewall(BaseDomain, DomainIdentityMixin):
    """Firewall Domain

    :param id: int
           ID of the Firewall
    :param name: str
           Name of the Firewall
    :param labels: dict
           User-defined labels (key-value pairs)
    :param rules: List[:class:`FirewallRule <hcloud.firewalls.domain.FirewallRule>`]
           Rules of the Firewall
    :param applied_to: List[:class:`FirewallResource <hcloud.firewalls.domain.FirewallResource>`]
           Resources currently using the Firewall
    :param created: datetime
           Point in time when the image was created
    """

    __api_properties__ = ("id", "name", "labels", "rules", "applied_to", "created")
    __slots__ = __api_properties__

    def __init__(
        self,
        id: int | None = None,
        name: str | None = None,
        labels: dict[str, str] | None = None,
        rules: list[FirewallRule] | None = None,
        applied_to: list[FirewallResource] | None = None,
        created: str | None = None,
    ):
        self.id = id
        self.name = name
        self.rules = rules
        self.applied_to = applied_to
        self.labels = labels
        self.created = isoparse(created) if created else None


class FirewallRule(BaseDomain):
    """Firewall Rule Domain

    :param direction: str
           The Firewall which was created
    :param port: str
           Port to which traffic will be allowed, only applicable for protocols TCP and UDP, specify port ranges by using
           - as a indicator, Sample: 80-85 means all ports between 80 & 85 (80, 82, 83, 84, 85)
    :param protocol: str
           Select traffic direction on which rule should be applied. Use source_ips for direction in and destination_ips for direction out.
    :param source_ips: List[str]
            List of permitted IPv4/IPv6 addresses in CIDR notation. Use 0.0.0.0/0 to allow all IPv4 addresses and ::/0 to allow all IPv6 addresses. You can specify 100 CIDRs at most.
    :param destination_ips: List[str]
           List of permitted IPv4/IPv6 addresses in CIDR notation. Use 0.0.0.0/0 to allow all IPv4 addresses and ::/0 to allow all IPv6 addresses. You can specify 100 CIDRs at most.
    :param description: str
           Short description of the firewall rule
    """

    __api_properties__ = (
        "direction",
        "port",
        "protocol",
        "source_ips",
        "destination_ips",
        "description",
    )
    __slots__ = __api_properties__

    DIRECTION_IN = "in"
    """Firewall Rule Direction In"""
    DIRECTION_OUT = "out"
    """Firewall Rule Direction Out"""

    PROTOCOL_UDP = "udp"
    """Firewall Rule Protocol UDP"""
    PROTOCOL_ICMP = "icmp"
    """Firewall Rule Protocol ICMP"""
    PROTOCOL_TCP = "tcp"
    """Firewall Rule Protocol TCP"""
    PROTOCOL_ESP = "esp"
    """Firewall Rule Protocol ESP"""
    PROTOCOL_GRE = "gre"
    """Firewall Rule Protocol GRE"""

    def __init__(
        self,
        direction: str,
        protocol: str,
        source_ips: list[str],
        port: str | None = None,
        destination_ips: list[str] | None = None,
        description: str | None = None,
    ):
        self.direction = direction
        self.port = port
        self.protocol = protocol
        self.source_ips = source_ips
        self.destination_ips = destination_ips or []
        self.description = description

    def to_payload(self) -> dict[str, Any]:
        """
        Generates the request payload from this domain object.
        """
        payload: dict[str, Any] = {
            "direction": self.direction,
            "protocol": self.protocol,
            "source_ips": self.source_ips,
        }
        if len(self.destination_ips) > 0:
            payload["destination_ips"] = self.destination_ips
        if self.port is not None:
            payload["port"] = self.port
        if self.description is not None:
            payload["description"] = self.description
        return payload


class FirewallResource(BaseDomain):
    """Firewall Used By Domain

    :param type: str
           Type of resource referenced
    :param server: Optional[Server]
           Server the Firewall is applied to
    :param label_selector: Optional[FirewallResourceLabelSelector]
           Label Selector for Servers the Firewall should be applied to
    :param applied_to_resources: (read-only) List of effective resources the firewall is
           applied to.
    """

    __api_properties__ = ("type", "server", "label_selector", "applied_to_resources")
    __slots__ = __api_properties__

    TYPE_SERVER = "server"
    """Firewall Used By Type Server"""
    TYPE_LABEL_SELECTOR = "label_selector"
    """Firewall Used By Type label_selector"""

    def __init__(
        self,
        type: str,
        server: Server | BoundServer | None = None,
        label_selector: FirewallResourceLabelSelector | None = None,
        applied_to_resources: list[FirewallResourceAppliedToResources] | None = None,
    ):
        self.type = type
        self.server = server
        self.label_selector = label_selector
        self.applied_to_resources = applied_to_resources

    def to_payload(self) -> dict[str, Any]:
        """
        Generates the request payload from this domain object.
        """
        payload: dict[str, Any] = {"type": self.type}
        if self.server is not None:
            payload["server"] = {"id": self.server.id}

        if self.label_selector is not None:
            payload["label_selector"] = {"selector": self.label_selector.selector}
        return payload


class FirewallResourceAppliedToResources(BaseDomain):
    """Firewall Resource applied to Domain

    :param type: Type of resource referenced
    :param server: Server the Firewall is applied to
    """

    __api_properties__ = ("type", "server")
    __slots__ = __api_properties__

    def __init__(
        self,
        type: str,
        server: BoundServer | None = None,
    ):
        self.type = type
        self.server = server


class FirewallResourceLabelSelector(BaseDomain):
    """FirewallResourceLabelSelector Domain

    :param selector: str Target label selector
    """

    def __init__(self, selector: str | None = None):
        self.selector = selector


class CreateFirewallResponse(BaseDomain):
    """Create Firewall Response Domain

    :param firewall: :class:`BoundFirewall <hcloud.firewalls.client.BoundFirewall>`
           The Firewall which was created
    :param actions: List[:class:`BoundAction <hcloud.actions.client.BoundAction>`]
           The Action which shows the progress of the Firewall Creation
    """

    __api_properties__ = ("firewall", "actions")
    __slots__ = __api_properties__

    def __init__(
        self,
        firewall: BoundFirewall,
        actions: list[BoundAction] | None,
    ):
        self.firewall = firewall
        self.actions = actions
