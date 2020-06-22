# -*- coding: utf-8 -*-
from hcloud.core.domain import BaseDomain, DomainIdentityMixin


class LoadBalancerType(BaseDomain, DomainIdentityMixin):
    """LoadBalancerType Domain

    :param id: int
           ID of the Load Balancer type
    :param name: str
           Name of the Load Balancer type
    :param description: str
           Description of the Load Balancer type
    :param max_connections: int
           Max amount of connections the Load Balancer can handle
    :param max_services: int
           Max amount of services the Load Balancer can handle
    :param max_targets: int
           Max amount of targets the Load Balancer can handle
    :param max_assigned_certificates: int
           Max amount of certificates the Load Balancer can serve
    :param prices: Dict
           Prices in different locations

    """

    __slots__ = (
        "id",
        "name",
        "description",
        "max_connections",
        "max_services",
        "max_targets",
        "max_assigned_certificates",
        "prices"
    )

    def __init__(
            self,
            id=None,
            name=None,
            description=None,
            max_connections=None,
            max_services=None,
            max_targets=None,
            max_assigned_certificates=None,
            prices=None
    ):
        self.id = id
        self.name = name
        self.description = description
        self.max_connections = max_connections
        self.max_services = max_services
        self.max_targets = max_targets
        self.max_assigned_certificates = max_assigned_certificates
        self.prices = prices
