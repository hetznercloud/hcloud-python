# -*- coding: utf-8 -*-
from dateutil.parser import isoparse

from hcloud.core.domain import BaseDomain


class Firewall(BaseDomain):
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

    __slots__ = ("id", "name", "labels", "rules", "applied_to", "created")

    def __init__(
        self, id=None, name=None, labels=None, rules=None, applied_to=None, created=None
    ):
        self.id = id
        self.name = name
        self.rules = rules
        self.applied_to = applied_to
        self.labels = labels
        self.created = isoparse(created) if created else None


class FirewallRule:
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

    __slots__ = (
        "direction",
        "port",
        "protocol",
        "source_ips",
        "destination_ips",
        "description",
    )

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
        direction,  # type: str
        protocol,  # type: str
        source_ips,  # type: List[str]
        port=None,  # type: Optional[str]
        destination_ips=None,  # type: Optional[List[str]]
        description=None,  # type: Optional[str]
    ):
        self.direction = direction
        self.port = port
        self.protocol = protocol
        self.source_ips = source_ips
        self.destination_ips = destination_ips or []
        self.description = description

    def to_payload(self):
        payload = {
            "direction": self.direction,
            "protocol": self.protocol,
            "source_ips": self.source_ips,
        }
        if len(self.destination_ips) > 0:
            payload.update({"destination_ips": self.destination_ips})
        if self.port is not None:
            payload.update({"port": self.port})
        if self.description is not None:
            payload.update({"description": self.description})
        return payload


class FirewallResource:
    """Firewall Used By Domain

    :param type: str
           Type of resource referenced
    :param server: Optional[Server]
           Server the Firewall is applied to
    :param label_selector: Optional[FirewallResourceLabelSelector]
           Label Selector for Servers the Firewall should be applied to
    """

    __slots__ = ("type", "server", "label_selector")

    TYPE_SERVER = "server"
    """Firewall Used By Type Server"""
    TYPE_LABEL_SELECTOR = "label_selector"
    """Firewall Used By Type label_selector"""

    def __init__(
        self,
        type,  # type: str
        server=None,  # type: Optional[Server]
        label_selector=None,  # type: Optional[FirewallResourceLabelSelector]
    ):
        self.type = type
        self.server = server
        self.label_selector = label_selector

    def to_payload(self):
        payload = {
            "type": self.type,
        }
        if self.server is not None:
            payload.update({"server": {"id": self.server.id}})

        if self.label_selector is not None:
            payload.update(
                {"label_selector": {"selector": self.label_selector.selector}}
            )
        return payload


class FirewallResourceLabelSelector(BaseDomain):
    """FirewallResourceLabelSelector Domain

    :param selector: str Target label selector
    """

    def __init__(self, selector=None):
        self.selector = selector


class CreateFirewallResponse(BaseDomain):
    """Create Firewall Response Domain

    :param firewall: :class:`BoundFirewall <hcloud.firewalls.client.BoundFirewall>`
           The Firewall which was created
    :param actions: List[:class:`BoundAction <hcloud.actions.client.BoundAction>`]
           The Action which shows the progress of the Firewall Creation
    """

    __slots__ = ("firewall", "actions")

    def __init__(
        self,
        firewall,  # type: BoundFirewall
        actions,  # type: BoundAction
    ):
        self.firewall = firewall
        self.actions = actions
