# -*- coding: utf-8 -*-
from dateutil.parser import isoparse

from hcloud.core.domain import BaseDomain


class Network(BaseDomain):
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
    :param servers: List[:class:`BoundServer <hcloud.servers.client.BoundServer>`]
           Servers attached to this network
    :param protection: dict
           Protection configuration for the network
    :param labels: dict
           User-defined labels (key-value pairs)
    """

    __slots__ = (
        "id",
        "name",
        "ip_range",
        "subnets",
        "routes",
        "servers",
        "protection",
        "labels",
        "created",
    )

    def __init__(
        self,
        id,
        name=None,
        created=None,
        ip_range=None,
        subnets=None,
        routes=None,
        servers=None,
        protection=None,
        labels=None,
    ):
        self.id = id
        self.name = name
        self.created = isoparse(created) if created else None
        self.ip_range = ip_range
        self.subnets = subnets
        self.routes = routes
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
    __slots__ = ("type", "ip_range", "network_zone", "gateway", "vswitch_id")

    def __init__(
        self, ip_range, type=None, network_zone=None, gateway=None, vswitch_id=None
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

    __slots__ = ("destination", "gateway")

    def __init__(self, destination, gateway):
        self.destination = destination
        self.gateway = gateway


class CreateNetworkResponse(BaseDomain):
    """Create Network Response Domain

    :param network: :class:`BoundNetwork <hcloud.networks.client.BoundNetwork>`
           The network which was created
    :param action: :class:`BoundAction <hcloud.actions.client.BoundAction>`
           The Action which shows the progress of the network Creation
    """

    __slots__ = ("network", "action")

    def __init__(
        self,
        network,  # type: BoundNetwork
        action,  # type: BoundAction
    ):
        self.network = network
        self.action = action
