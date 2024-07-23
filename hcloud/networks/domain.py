from __future__ import annotations

from typing import TYPE_CHECKING

from dateutil.parser import isoparse

from ..core import BaseDomain, DomainIdentityMixin

if TYPE_CHECKING:
    from ..actions import BoundAction
    from ..servers import BoundServer
    from .client import BoundNetwork


class Network(BaseDomain, DomainIdentityMixin):
    """Network Domain

    :param id: int
           ID of the network
    :param name: str
           Name of the network
    :param ip_range: str
           IPv4 prefix of the whole network
    :param subnets: List[:class:`NetworkSubnet <hcloud.networks.domain.NetworkSubnet>`]
           Subnets allocated in this network
    :param routes: List[:class:`NetworkRoute <hcloud.networks.domain.NetworkRoute>`]
           Routes set in this network
    :param expose_routes_to_vswitch: bool
           Indicates if the routes from this network should be exposed to the vSwitch connection.
    :param servers: List[:class:`BoundServer <hcloud.servers.client.BoundServer>`]
           Servers attached to this network
    :param protection: dict
           Protection configuration for the network
    :param labels: dict
           User-defined labels (key-value pairs)
    """

    __api_properties__ = (
        "id",
        "name",
        "ip_range",
        "subnets",
        "routes",
        "expose_routes_to_vswitch",
        "servers",
        "protection",
        "labels",
        "created",
    )
    __slots__ = __api_properties__

    def __init__(
        self,
        id: int,
        name: str | None = None,
        created: str | None = None,
        ip_range: str | None = None,
        subnets: list[NetworkSubnet] | None = None,
        routes: list[NetworkRoute] | None = None,
        expose_routes_to_vswitch: bool | None = None,
        servers: list[BoundServer] | None = None,
        protection: dict | None = None,
        labels: dict[str, str] | None = None,
    ):
        self.id = id
        self.name = name
        self.created = isoparse(created) if created else None
        self.ip_range = ip_range
        self.subnets = subnets
        self.routes = routes
        self.expose_routes_to_vswitch = expose_routes_to_vswitch
        self.servers = servers
        self.protection = protection
        self.labels = labels


class NetworkSubnet(BaseDomain):
    """Network Subnet Domain

    :param type: str
              Type of sub network.
    :param ip_range: str
              Range to allocate IPs from.
    :param network_zone: str
              Name of network zone.
    :param gateway: str
              Gateway for the route.
    :param vswitch_id: int
              ID of the vSwitch.
    """

    TYPE_SERVER = "server"
    """Subnet Type server, deprecated, use TYPE_CLOUD instead"""
    TYPE_CLOUD = "cloud"
    """Subnet Type cloud"""
    TYPE_VSWITCH = "vswitch"
    """Subnet Type vSwitch"""

    __api_properties__ = ("type", "ip_range", "network_zone", "gateway", "vswitch_id")
    __slots__ = __api_properties__

    def __init__(
        self,
        ip_range: str,
        type: str | None = None,
        network_zone: str | None = None,
        gateway: str | None = None,
        vswitch_id: int | None = None,
    ):
        self.type = type
        self.ip_range = ip_range
        self.network_zone = network_zone
        self.gateway = gateway
        self.vswitch_id = vswitch_id


class NetworkRoute(BaseDomain):
    """Network Route Domain

    :param destination: str
           Destination network or host of this route.
    :param gateway: str
           Gateway for the route.
    """

    __api_properties__ = ("destination", "gateway")
    __slots__ = __api_properties__

    def __init__(self, destination: str, gateway: str):
        self.destination = destination
        self.gateway = gateway


class CreateNetworkResponse(BaseDomain):
    """Create Network Response Domain

    :param network: :class:`BoundNetwork <hcloud.networks.client.BoundNetwork>`
           The network which was created
    :param action: :class:`BoundAction <hcloud.actions.client.BoundAction>`
           The Action which shows the progress of the network Creation
    """

    __api_properties__ = ("network", "action")
    __slots__ = __api_properties__

    def __init__(
        self,
        network: BoundNetwork,
        action: BoundAction,
    ):
        self.network = network
        self.action = action
