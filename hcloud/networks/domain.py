# -*- coding: utf-8 -*-
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
        "labels"
    )

    def __init__(
            self,
            id=None,
            name=None,
            ip_range=None,
            subnets=None,
            routes=None,
            servers=None,
            protection=None,
            labels=None

    ):
        self.id = id
        self.name = name
        self.ip_range = ip_range
        self.subnets = subnets
        self.routes = routes
        self.servers = servers
        self.protection = protection
        self.labels = labels


class NetworkSubnet(BaseDomain):
    #  TODO
    pass


class NetworkRoute(BaseDomain):
    #  TODO
    pass


class CreateNetworkResponse(BaseDomain):
    """Create Network Response Domain

    :param network: :class:`BoundNetwork <hcloud.networks.client.BoundNetwork>`
           The network which was created
    :param action: :class:`BoundAction <hcloud.actions.client.BoundAction>`
           The Action which shows the progress of the network Creation
    """
    __slots__ = (
        "network",
        "action"
    )

    def __init__(
            self,
            network,  # type: BoundNetwork
            action,  # type: BoundAction
    ):
        self.network = network
        self.action = action
